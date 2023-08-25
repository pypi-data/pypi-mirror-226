from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jabor',
    description='a collective utilities for python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jabor AlMusalam',
    author_email='jabor@jabor.me',
    keywords='python utils',
    version='0.0.5',
    license='MIT License',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules = ["jabor"],
    python_requires=">=3.8",
    url="https://github.com/jaborsm/jabor",
    project_urls={
        'Bug Tracker': 'https://github.com/jaborsm/jabor/issues',
        'Source Code': 'https://github.com/jaborsm/jabor',
        # 'Documentation': 'https://github.com/tomchen/example_pypi_package',

    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
