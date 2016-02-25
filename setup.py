import re
import os
import codecs

from setuptools import setup, find_packages


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='dockercloud-workerlistgen',
    version=find_version('workerlistgen', '__init__.py'),
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['dockercloud-workerlistgen = workerlistgen.main:main']
    },
    include_package_data=True,
    author='Docker, Inc.',
    author_email='info@docker.com',
    description='Auto self-configured workerlistgen on Docker Cloud',
    license='Apache v2',
    keywords='docker cloud workerlistgen',
    url='http://cloud.docker.com/',
)
