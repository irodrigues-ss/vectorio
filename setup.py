from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='vectorio',
    version='1.2.5',
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
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation ",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires='>=3.6',
    zip_safe=False,
)