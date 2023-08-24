from setuptools import setup, find_packages

setup(
    name='shipdan_model-test2',
    version='3.6.1',
    description='model package for shipdan business written by Bunkerkids Tech',
    author='bunkerkids',
    author_email='development@bunkerkids.net',
    url='https://github.com/bunkerkids/shipdan_model',
    install_requires=['django'],
    packages=find_packages(exclude=['shipdan_model.shipdan_model']),
)