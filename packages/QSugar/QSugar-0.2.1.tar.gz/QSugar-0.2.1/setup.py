from setuptools import setup, find_packages

setup(
    name="QSugar",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "Qt.py", "QBinder"
    ],
    author="Attic",
    author_email="mornorrisjie@gmail.com",
    description="PyQt/PySide framework, dedicated to more modern UI design. Based on interface injection, achieve separation of interface and data, as well as hierarchical layout design. It is recommended to use it in conjunction with the QBinder framework.",
    long_description=open("README.md",encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/AtticRat/QSugar",
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
