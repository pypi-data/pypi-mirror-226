import sys
from os import path

from funbuild.tool import read_version
from setuptools import find_packages, setup

version_path = path.join(path.abspath(path.dirname(__file__)), "script/__version__.md")

version = read_version(version_path)


install_requires = ["requests", "funsecret", "tqdm", "requests_toolbelt", "lanzou-api"]


setup(
    name="fundrive",
    version=version,
    description="fundrive",
    author="bingtao",
    author_email="1007530194@qq.com",
    url="https://github.com/1007530194",
    packages=find_packages(),
    install_requires=install_requires,
)
