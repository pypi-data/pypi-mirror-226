import re

from setuptools import setup


def pantherdb_version() -> str:
    with open('pantherdb/__init__.py') as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


VERSION = pantherdb_version()
with open('README.md') as file:
    DESCRIPTION = file.read()

setup(
    name='pantherdb',
    version=VERSION,
    python_requires='>=3.8',
    author='Ali RajabNezhad',
    author_email='alirn76@yahoo.com',
    url='https://github.com/alirn76/pantherdb',
    description='is a Simple, FileBase and Document Oriented database',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'orjson~=3.9.5',
        'cryptography~=41.0',
    ],
)
