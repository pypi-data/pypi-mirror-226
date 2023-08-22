from setuptools import setup, find_packages
import os

setup(
    name = "swavey",
    version = "0.0.2",
    author = "Ian Lai",
    author_email = "",
    description = ("Test"),
    packages=find_packages(),
    install_requires=["requests", "bs4", "random", "datetime", "flask"],
    keywords=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)