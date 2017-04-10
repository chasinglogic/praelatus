from setuptools import setup

setup(
    name='praelatus',
    packages=['praelatus'],
    install_requires=open('./requirements.txt').split('\n')
)
