#!/usr/bin/env python

import os
from distutils.cmd import Command
from distutils.core import setup
from distutils.errors import DistutilsExecError

class Install(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            os.system("/bin/echo -e 'Setting up SSHMonitor'")
            os.system('/bin/bash sshmonitor/build/build.sh install')
        except DistutilsExecError:
            self.warn('Error setting up SSHMonitor!')

class Remove(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            os.system("/bin/echo -e 'Removing SSHMonitor'")
            os.system('/bin/bash sshmonitor/build/build.sh remove')
        except DistutilsExecError:
            self.warn('Error removing SSHMonitor!')

setup(
    name='sshmonitor',
    version='0.0.2',
    author='Anthony Guevara',
    author_email='amboxer21@gmail.com',
    license='GPL-3.0',
    url='https://github.com/amboxer21/SSHMonitorPy',
    packages=[],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Development Status :: 2 - Beta',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License (GPL)', 
    ],
    cmdclass={
        'install': Install,
        'remove': Remove
    },
)
