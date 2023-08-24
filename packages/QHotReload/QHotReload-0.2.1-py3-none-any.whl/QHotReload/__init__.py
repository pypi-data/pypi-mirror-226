import ast
import difflib
import hashlib
import logging

from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *


def Reload(ReloadClass):
    return ReloadClass


class FileChangeWatcher(QObject):
    file_changed = Signal(str)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self._hash = self._calculate_hash()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_file)

    def _calculate_hash(self):
        sha1 = hashlib.sha1()
        with open(self.filename, 'rb') as f:
            while chunk := f.read(65536):
                sha1.update(chunk)
        return sha1.hexdigest()

    def start(self, interval=1000):
        self.timer.start(interval)

    def check_file(self):
        new_hash = self._calculate_hash()
        if new_hash != self._hash:
            self._hash = new_hash
            self.file_changed.emit(self.filename)


class ReloadProcessor(QObject):
    def __init__(self):
        super().__init__()
        self.last_code = ''

    def reload(self, filename):
        logging.info('reloading')
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                source_code = file.read()

            reload_classes = []
            tree = ast.parse(source_code)

            import_nodes = []
            exclude_lib = ['PyQt', 'PySide', 'QHotReload']

            for node in ast.walk(tree):
                if isinstance(node, ast.Module):
                    for body_node in node.body:
                        if isinstance(body_node, ast.Import):
                            import_nodes.append(body_node)

                        if isinstance(body_node, ast.ImportFrom):
                            import_from_code = ast.unparse(body_node)
                            append_flag = True
                            for lib in exclude_lib:
                                if lib in import_from_code:
                                    append_flag = False
                                    break
                            if append_flag:
                                import_nodes.append(body_node)

                if isinstance(node, ast.ClassDef):
                    for decorator in node.decorator_list:
                        if decorator.id == 'Reload':
                            disp_code = ast.unparse(node)

                            for body_node in node.body:
                                if isinstance(body_node, ast.FunctionDef):
                                    if body_node.name == '__init__':
                                        for import_node in import_nodes:
                                            body_node.body.insert(0, import_node)

                            exec_code = ast.unparse(node)

                            diff = difflib.ndiff(self.last_code.splitlines(), disp_code.splitlines())
                            diff_text = '\n'.join(list(diff))
                            logging.info(f'show difference\n {diff_text}')
                            self.last_code = disp_code
                            exec(exec_code)
                            reload_classes.append(node.name)

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                            if node.value.func.id in reload_classes:
                                obj_name = node.targets[0].id
                                obj_class_name = node.value.func.id

                                logging.debug(f'affected object <class:{obj_class_name} object:{obj_name}>')

                                cls = eval(obj_class_name)

                                globals()[obj_name].close()
                                globals()[obj_name].deleteLater()
                                del globals()[obj_name]

                                globals()[obj_name] = cls()
                                globals()[obj_name].setWindowFlag(Qt.WindowStaysOnTopHint)
                                globals()[obj_name].show()
        except Exception as e:
            logging.error(e.args)


class SingletonCaller:
    def __init__(self):
        pass

    def __call__(self, filename):
        self.processor = ReloadProcessor()
        self.watcher = FileChangeWatcher(filename)
        self.watcher.file_changed.connect(self.processor.reload)
        self.watcher.start()  # 启动定时器监视文件变化

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG
        )


watch = SingletonCaller()
