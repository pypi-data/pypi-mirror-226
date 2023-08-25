from setuptools import setup, find_packages

setup(
    name='jabor',
    description='a collective utilities for python',
    author='Jabor AlMusalam',
    author_email='jabor@jabor.me',
    keywords='jabor jabor',
    version='0.0.1',
    license='MIT License',
    packages=find_packages(),
    install_requires=[
        'datetime',
    ],
    python_requires='>=3.10'
)