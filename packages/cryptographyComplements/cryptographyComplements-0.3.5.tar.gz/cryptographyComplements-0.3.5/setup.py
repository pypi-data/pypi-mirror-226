from setuptools import setup, find_packages
import decimal

setup(
    name='cryptographyComplements',
    version='0.3.5',
    description='A Python library, in development, that allows the user to use cryptography, and related, functions.',
    long_description='A Python library, in development, that allows the user to use cryptography, and related, functions.',
    long_description_content_type='text/markdown',
    author='Forzo',
    packages=find_packages(),
    license="GPL-3.0",
    project_urls={
        'Source': 'https://github.com/Forzooo/cryptographyComplements',
        'Documentation': 'https://cryptographycomplements.readthedocs.io/'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)