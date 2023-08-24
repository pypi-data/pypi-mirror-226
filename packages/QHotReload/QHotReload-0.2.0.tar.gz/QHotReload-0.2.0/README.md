# QHotReload
Hot relading tool for PySide and PyQt

![GIF 2023-8-21 11-44-32](https://github.com/AtticRat/PyQHotReload/assets/129368033/44850b2f-40f3-4f70-a0c0-66e7af0aa017)


# Other Language

- en [English](README.md)
- zh_CN [简体中文](README.zh_CN.md)

# Usage
To load the main body of the Qt window, please wrap the QWigdet or QMainWindow you defined with `Reload`,e.g.
```python
@Reload
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # ...
```

Meanwhile, after your window is showed, use the `watch` functor to listen to the current Python file，
Then expose the window variable to the global namespace of `QHotReload` module,e.g.

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    QHotReload.window = window
    watch(__file__)

    app.exec_()
```

# Examples
Please check out `example.py`
