#!/usr/bin/env python

import re
import sys
import subprocess

class Version(object):

    @staticmethod
    def python():
        python_version = re.search('\d\.\d\.\d', str(sys.version), re.I | re.M)
        if python_version is not None:
            return python_version.group()
        return "None"

    @staticmethod
    def python_is_version(version=None):
        if re.search('^'+str(version)+'\.\d+\.\d+', str(Version.python()), re.M | re.I) is None:
            return False
        return True
        
    @staticmethod
    def release():
        comm = subprocess.Popen(["lsb_release -irs"], shell=True, stdout=subprocess.PIPE)
        return re.search("(\w+)", str(comm.stdout.read())).group()

    @staticmethod
    def system_package_manager():
        package_manager = {
            'rpm': ('centos','fedora','scientific','opensuse'),
            'apt': ('debian','ubuntu','linuxmint'),
            'eix': ('gentoo',)
        }
        for key,value in package_manager.items():
            manager = re.search(Version.release().lower(),str(value), re.I | re.M)
            if manager is not None:
                return key
