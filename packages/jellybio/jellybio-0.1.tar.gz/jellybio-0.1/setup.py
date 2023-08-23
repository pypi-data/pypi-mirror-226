# setup.py

from setuptools import setup, find_packages

setup(
    name='jellybio',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # list your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)

