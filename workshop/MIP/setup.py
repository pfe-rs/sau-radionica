from distutils.core import setup
from setuptools import find_packages

setup(
    name='nepoznati_model',
    description='Nepoznati model',
    version='0.1.0',
    author='PFE',
    author_email='kontakt@pfe.rs',
    packages=find_packages(),
    package_data={'': ['*.*']},
    license=None,
    install_requires=[
        'scikit-learn',
        'scikit-image',
        'numpy',
        'matplotlib',
        'scipy',
        'control'
    ],
)
