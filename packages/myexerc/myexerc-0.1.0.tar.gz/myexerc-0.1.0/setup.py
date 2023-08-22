from setuptools import setup, find_packages

setup(
    name="myexerc",
    version="0.1.0",
    py_modules=["main"],
    author="Patchu",
    packages=find_packages(),
    install_requires=[
        "Click",  # If you are using Typer, it's built on top of Click, so it's required.
    ],
    entry_points={
        "console_scripts": [
            "myexerc = main:app",
        ],
    },
)
