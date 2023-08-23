from setuptools import setup, find_packages

setup(
    name='tdf-anonymizer',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'pydantic',
        'faker',
        'pandas'
    ],
)
