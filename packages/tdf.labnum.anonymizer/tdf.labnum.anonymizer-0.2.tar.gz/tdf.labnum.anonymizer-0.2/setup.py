from setuptools import setup, find_packages

setup(
    name='tdf.labnum.anonymizer',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'pydantic',
        'faker',
        'pandas'
    ],
)
