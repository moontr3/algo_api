from setuptools import setup, find_packages

setup(
    name='algo_api',
    version='0.0.1',
    description='Algoritmika Student API',
    author='moontr3',
    packages=find_packages(),
    install_requires=['requests'],
    zip_safe=False
)