"""Build a Praelatus release tarball"""

import argparse
import subprocess
import os

FILE_LIST = [
    'fields',
    'labels',
    'praelatus',
    'profiles',
    'schemes',
    'static',
    'templates',
    'tickets',
    'workflows',
    'scripts/praelatus.sh',
]


def build_static_assets():
    subprocess.run(['webpack'])


def build(version, release_name):
    build_static_assets()

    if os.path.exists('dist'):
        os.rmdir('dist')

    os.mkdir('dist')
    for fil in FILE_LIST:
        subprocess.run(['cp', '-R', fil, 'dist/'])

    if release_name != '':
        tar_name = 'praleatus-v{}-r{}.tar.gz'.format(version, release_name)
    else:
        tar_name = 'praleatus-v{}.tar.gz'.format(version)

    subprocess.run(['tar', 'czvf', 'dist/*', tar_name])


def main():
    git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])

    parser = argparse.ArgumentParser(description='Build a Praelatus release tarball')
    parser.add_argument('-v', '--version', default=git_hash, help='The version number')
    parser.add_argument('-r', '--release-name', dest='release_name',
                        default='', help='The release name')
    args = parser.parse_args()

    build(args.version, args.release_name)


if __name__ == '__main__':
    main()
