import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

print(setuptools.find_packages())

setuptools.setup(
    name='SauLib',
    version='0.0.1',
    author='PFE',
    author_email='kontakt@pfe.rs',
    description='Library for practicing SAU',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
)
