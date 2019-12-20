from setuptools import setup, find_packages

setup(name='vectorio',
    version='1.0.0',
    description='utility for working with vector data',
    author='Igor Rodrigues Sousa Silva',
    author_email='igor.rodrigues.ss10@gmail.com',
    url='https://github.com/igor-rodrigues-ss/vectorio',
    test_suite='tests',
    packages=find_packages(exclude='tests'),
    tests_require=['pytest'],
    install_requires=[
        'rarfile==3.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

# sudo apt-get install unrar
# pip install gdal==2.2
# install gdal
