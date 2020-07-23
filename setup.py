#!/usr/bin/env python

import re
import os
import sys
import time
import subprocess

from src.lib.logging.logger import Logging as Logger
from src.lib.version.version import Version as Version

from ctypes import cdll
from distutils.cmd import Command
from setuptools import setup, find_packages
from subprocess import Popen, call, PIPE, STDOUT
from distutils.errors import DistutilsError, DistutilsExecError

class Check(object):

    def __init__(self):

        self.sys_dependencies = {
            'rpm': (
                'gtk+-devel','gtk2-devel',
                'python-devel','syslog-ng',
            ),
            'eix': (
                'x11-libs/gtk+:2','x11-libs/gtk+:3',
                'app-admin/syslog-ng','dev-lang/python',
            ),
            'apt': (
                'libgtk2.0-dev','python-dev','syslog-ng',
            )
        }

        self.package_manager = {
            'rpm': ('centos','fedora','scientific','opensuse'),
            'apt': ('debian','ubuntu','linuxmint'),
            'eix': ('gentoo',)
        }

    def system_query_command(self):
        if 'rpm' in  Version.system_package_manager():
            system_query_command = 'rpm -qa'
        elif 'apt' in Version.system_package_manager():
            system_query_command = 'dpkg --get-selections'
        elif 'eix' in Version.system_package_manager():
            system_query_command = 'eix -e --only-names'
        return system_query_command

    def grep_system_packages(self,package_name):
        comm = subprocess.Popen([self.system_query_command()
            + " " + str(package_name)], shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read()
        if not len(comm.strip()) == 0:
            Logger.log("INFO", "Package "
                + str(package_name)
                + " was found.")
        else:
            Logger.log("ERROR", "Package "
                + str(package_name)
                + " was not found.")

    def main(self):
        try:
            for item in self.sys_dependencies[Version.system_package_manager()]:
                self.grep_system_packages(item)
        except DistutilsExecError as distutilsExecError:
            Logger.log("ERROR", "Exception DistutilsExecError: "
                + str(distutilsExecError))

class PrepareBuild(object):

    def __init__(self,*args,**kwargs):
        cdll.LoadLibrary(args[0]).build()

if __name__ == '__main__':

    path = str(os.getcwd()) + '/src/lib/shared/libbuild.so'

    Logger.log('INFO','Checking system dependencies.')
    check = Check()
    check.main()

    Logger.log('INFO','Building libraries.')
    path = str(os.getcwd()) + '/src/lib/shared/libbuild.so'
    cdll.LoadLibrary(path).build()

    Logger.log('INFO','Entering setup in setup.py')

    setup(name='sshmonitor',
    version='2.0.0',
    url='https://github.com/amboxer21/SSHMonitor',
    license='GPL-3.0',
    author='Anthony Guevara',
    author_email='amboxer21@gmail.com',
    description="Monitors incoming ssh requests and will notify you on failed, successful or "
        + "banned(IP via iptables/sshgaurd) attempts whether they're successful or not.",
    packages=find_packages(exclude=['tests']),
    #long_description=open('README.md').read(),
    #long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    data_files=[
        ('/usr/lib/', ['src/lib/shared/libmasquerade.so']),
        ('/usr/local/bin/', ['src/notify-gtk']),
        ('/usr/local/bin/', ['src/sshmonitor.py'])],
    zip_safe=True,)
