from setuptools import setup, find_packages

setup(
    name='py_mrm',
    version='1.1.0',
    author='E.A.J.F. Peters',
    author_email='e.a.j.f.peters@tue.nl',
    description='Function for multiphase reactor modeling',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
)
