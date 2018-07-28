#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['vialectrum.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/vialectrum.png'])
    ]

extras_require = {
    'hardware': requirements_hw,
    'fast': ['pycryptodomex', 'scrypt>=0.6.0'],
    ':python_version < "3.5"': ['typing>=3.0.0'],
}
extras_require['full'] = extras_require['hardware'] + extras_require['fast']


setup(
    name="Vialectrum",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require=extras_require,
    packages=[
        'vialectrum',
        'vialectrum_gui',
        'vialectrum_gui.qt',
        'vialectrum_plugins',
        'vialectrum_plugins.audio_modem',
        'vialectrum_plugins.cosigner_pool',
        'vialectrum_plugins.email_requests',
        'vialectrum_plugins.hw_wallet',
        'vialectrum_plugins.keepkey',
        'vialectrum_plugins.labels',
        'vialectrum_plugins.ledger',
        'vialectrum_plugins.revealer',
        'vialectrum_plugins.trezor',
        'vialectrum_plugins.digitalbitbox',
        'vialectrum_plugins.virtualkeyboard',
    ],
    package_dir={
        'vialectrum': 'lib',
        'vialectrum_gui': 'gui',
        'vialectrum_plugins': 'plugins',
    },
    package_data={
        '': ['*.txt', '*.json', '*.ttf', '*.otf'],
        'vialectrum': [
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ],
    },
    scripts=['vialectrum'],
    data_files=data_files,
    description="Lightweight Viacoin Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="http://vialectrum.org",
    long_description="""Lightweight Viacoin Wallet"""
)
