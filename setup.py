from os import path
from setuptools import setup, find_packages

install_requires = []
if path.isfile('requirements.txt'):
    with open('requirements.txt') as f:
        install_requires = f.read().splitlines()

setup(
    name='uno-simulation',
    version='1.0',
    packages=find_packages(),
    install_requires=install_requires,
    url='https://github.com/AllehGonj/uno-simulation',
    license='MIT',
    author='alejandro',
    author_email='alejandrogonzalr@gmail.com',
    description='UNO card simulation'
)
