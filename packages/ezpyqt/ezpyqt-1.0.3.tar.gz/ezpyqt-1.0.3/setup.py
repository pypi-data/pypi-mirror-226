from setuptools import setup, find_packages

__version__ = "1.0.3"

setup(
    name="ezpyqt",
    version=__version__,
    description="To make the use of PyQt easier, Hence the name ezpyqt!",
    author="Saeid Alizadeh",
    author_email="saeidalz96@gmail.com",
    url="https://github.com/saeidalz13/ezpyqt",
    packages=find_packages(),
    install_requires=[
        "PySide6",
    ],
)
