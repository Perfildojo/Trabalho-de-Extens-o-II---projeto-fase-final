# setup.py
from setuptools import setup, find_packages

setup(
    name="mapa_do_medo_bot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.0",  # Versão mínima 20.0
        "pandas>=1.0"                 # Versão mínima 1.0
    ],
)