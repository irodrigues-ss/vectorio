from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='vectorio',
    version='1.2.0',
    description='Geoprocessing utility for working with vector data',
    author='Igor Rodrigues Sousa Silva',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='igor.rodrigues.ss10@gmail.com',
    url='https://github.com/igor-rodrigues-ss/vectorio',
    test_suite='tests',
    packages=find_packages(exclude='tests'),
    tests_require=['pytest'],
    install_requires=[
        'rarfile==3.1',
    ],
    data_files=[('assets', ['assets/World_UTM_Grid_HM.zip'])],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)