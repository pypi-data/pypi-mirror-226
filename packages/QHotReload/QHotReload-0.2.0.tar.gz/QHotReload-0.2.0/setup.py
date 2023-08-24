from setuptools import setup, find_packages

setup(
    name="QHotReload",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "qtpy"
    ],
    author="Attic",
    author_email="mornorrisjie@gmail.com",
    description="Hot relading tool for PySide and PyQt",
    long_description=open("README.md",encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/AtticRat/PyQHotReload",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)