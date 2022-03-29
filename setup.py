#!/usr/bin/env python
import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='celery-farmer',
    version='0.2.1',
    author='Wolt Enterprises Oy',
    author_email='support@wolt.com',
    description='Farmer will monitor how the Celery cluster is behaving',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/woltapp/celery-farmer',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    install_requires=[
        'statsd>=3.2.0,<4.0',
        'redis>=2.10.0,<4.0',
        'celery>=4.0,<6.0',
        'click>=6.7,<9.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points=dict(
        console_scripts='celery-farmer = celery_farmer.cli:cli'
    ),
)
