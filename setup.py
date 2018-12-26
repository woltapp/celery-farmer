#!/usr/bin/env python
import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='farmer',
    version='0.1.0',
    author='Wolt Enterprises Oy',
    author_email='support@wolt.com',
    description='Farmer will monitor how the Celery cluster is behaving',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/woltapp/farmer',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'statsd>=3.2.0,<4.0',
        'redis>=2.10.0,<4.0',
        'celery>=4.0,<5.0',
        'click>=6.7,<8.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points=dict(
        console_scripts='farmer = farmer.cli:cli'
    ),
)
