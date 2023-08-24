from setuptools import find_packages
from setuptools import setup

name = 'torchnyan'

setup(
    name=name,
    version='0.1.2',
    packages=[package for package in find_packages() if package.startswith(name)],
    url='https://github.com/speedcell4/torchnyan',
    license='MIT',
    author='speedcell4',
    author_email='speedcell4@gmail.com',
    python_requires='>=3.9',
    install_requires=[],
)
