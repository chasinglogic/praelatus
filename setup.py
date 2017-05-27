# noqa: D100
import os
import re
from setuptools import setup

praelatusfile = os.path.join(os.path.dirname(__file__),
                             'src', 'praelatus', '__init__.py')

# Thanks to SQLAlchemy:
# https://github.com/zzzeek/sqlalchemy/blob/master/setup.py#L104
with open(praelatusfile) as stream:
    __version__ = re.compile(
        r".*__version__ = '(.*?)'", re.S
    ).match(stream.read()).group(1)


# Thanks to Pagure:
# https://pagure.io/pagure/blog/master/f/setup.py
def get_requirements():
    """
    Get the contents of a file listing the requirements.

    Returns:
        the list of requirements, or an empty list if
        `requirements_file` could not be opened or read
    :return type: list
    """
    import platform

    if platform.python_implementation() == 'PyPy':
        requirements_file = 'requirements_pypy.txt'
    else:
        requirements_file = 'requirements.txt'

    with open(requirements_file) as f:
        return [
            line.rstrip().split('#')[0]
            for line in f.readlines()
            if not line.startswith('#')
        ]


setup(
    name='praelatus',
    description='An Open Source bug tracking / ticketing system',
    version=__version__,
    packages=[
        'praelatus',
    ],
    package_dir={'': 'src'},
    package_data={
        'praelatus': ['templates/*',
                      'migrations/*',
                      'static/*']
    },
    include_package_data=True,
    author="""Mathew Robinson and many others.""",
    author_email="team@praelatus.io",
    url='https://prealatus.io',
    download_url='https://github.com/praelatus/praelatus/releases',
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'praelatus = praelatus.cli:cli'
        ]
    },
    license='Apache2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Bug Tracking',
    ]
)
