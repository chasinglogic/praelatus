from setuptools import setup

setup(
    name='praelatus',
    packages=['praelatus'],
    install_requires=[
        'flask',
        'sqlalchemy',
        'flask-sqlalchemy'
        'psycopg2',
        'celery'
    ]
)
