from setuptools import setup

setup(
    name='praelatus',
    packages=['praelatus'],
    install_requires=open('./requirements.txt').read().split('\n'),
    entry_points={
        'console_scripts': [
            'praelatus = praelatus.cli:cli'
        ]
    }
)
