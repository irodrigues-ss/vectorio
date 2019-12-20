from setuptools import setup, find_packages

setup(name='vectorio',
    version='1.0.0',
    description='utility for working with vector data',
    author='Igor Rodrigues Sousa Silva',
    author_email='igor.rodrigues.ss10@gmail.com',
    url='http://teste.com',
    test_suite='tests',
    packages=find_packages(exclude='tests'),
    tests_require=['pytest'],
    install_requires=[
        'rarfile==3.1',
    ]
)

# sudo apt-get install unrar
# pip install gdal==2.2
# install gdal
