from os import path

from funbuild.tool import read_version
from setuptools import find_packages, setup


install_requires = ["tqdm"]


setup(
    name="funfile",
    version=read_version(path.join(path.abspath(path.dirname(__file__)), "script/__version__.md")),
    description="funfile",
    author="niuliangtao",
    author_email="1007530194@qq.com",
    url="https://github.com/1007530194",
    packages=find_packages(),
    install_requires=install_requires,
)
