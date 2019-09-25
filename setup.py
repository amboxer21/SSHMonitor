#!/usr/bin/env python

import re
import os
import sys
import time
import subprocess

import src.lib.gdm.gdm as gdm
import src.lib.version.version as version

from src.lib.logging.logger import Logging as Logger

from distutils.cmd import Command
from optparse import OptionParser
from subprocess import Popen, call, PIPE
from setuptools import setup, find_packages
from distutils.errors import DistutilsError, DistutilsExecError

class Check(object):

    def __init__(self):
        self.sys_dependencies = {
            'rpm': (
                'gtk+-devel','gtk2-devel','python-devel',
                'syslog-ng','sendmail-cf','sendmail-devel','procmail'
            ),
            'eix': (
                'x11-libs/gtk+:2','x11-libs/gtk+:3','mail-filter/procmail',
                'mail-mta/sendmail','app-admin/syslog-ng','dev-lang/python',
            ),
            'apt': (
                'libgtk2.0-dev','python-dev','procmail','sendmail-bin',
                'sendmail-cf','sensible-mda','syslog-ng','sendmail-base',
            )
        }
        self.package_manager = {
            'rpm': ('centos','fedora','scientific','opensuse'),
            'apt': ('debian','ubuntu','linuxmint'),
            'eix': ('gentoo',)
        }

    def system_query_command(self):
        if 'rpm' in  version.system_package_manager():
            system_query_command = 'rpm -qa'
        elif 'apt' in version.system_package_manager():
            system_query_command = 'dpkg --get-selections'
        elif 'eix' in version.system_package_manager():
            system_query_command = 'eix -e --only-names'
        return system_query_command

    def grep_system_packages(self,package_name):
        comm = subprocess.Popen([self.system_query_command()
            + " " + str(package_name)], shell=True,
            stdout=subprocess.PIPE).stdout.read().strip()
        if len(comm) > 0:
            Logger.log("INFO", "Package "
                + str(comm)
                + " was found.")
        else:
            Logger.log("ERROR", "Package "
                + str(package_name)
                + " was not found.")

    def main(self):
        try:
            for item in self.sys_dependencies[version.system_package_manager()]:
                self.grep_system_packages(item)
        except DistutilsExecError as distutilsExecError:
            Logger.log("ERROR", "Exception DistutilsExecError: "
                + str(distutilsExecError))

class PrepareBuild(object):

    def __init__(self,setup_options={},config_dict={}):

        self.check    = setup_options['check']
        self.build    = setup_options['build']
        self.sdist    = setup_options['sdist']
        self.install  = setup_options['install']

        self.email    = config_dict['email']
        self.password = config_dict['password']

    def cron_tab(self):
        #Count need to be 1 in order to write to the crontab.
        #Basically, checking for grep being None or not None will 
        #not work in this case and we need to check for 2 occurances.
        count=0
        command="/bin/bash /home/root/.ssh/is_sshm_running.sh"
        cron = CronTab(user='root')
        job = cron.new(command=command)
        job.minute.every(1)
        for job in cron:
            grep = re.search(r'\/is_sshm_running.sh', str(job))
            if grep is not None:
                count+=1
        if count < 2 and self.install:
            Logger.log("INFO", "Installing crontab.")
            cron.write()
            print("Please nesure that the crontab was actually installed!")
            print("To do so please run(without quotes) => 'sudo crontab -l -u root'")

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option(
        '--check', dest='check', action="store_true", default=False
    )
    parser.add_option(
        '--build', dest='build', action="store_true", default=False
    )
    parser.add_option(
        '--sdist', dest='sdist', action="store_true", default=False
    )
    parser.add_option(
        '--install', dest='install', action="store_true", default=False
    )
    parser.add_option('-e', '--email',
        dest='email', default='sshmonitorapp@gmail.com',
        help='This argument is required unless you pass the '
            + 'pass the --disable-email flag on the command line. '
            + 'Your E-mail address is used to notify you that'
            + 'there is activity related to ssh attempts.')
    parser.add_option('-p', '--password',
        dest='password', default='hkeyscwhgxjzafvj',
        help='This argument is required unless you pass the '
            + 'pass the --disable-email flag on the command line. '
            + 'Your E-mail password is used to send an E-mail of the ip '
            + 'of the user sshing into your box, successful or not.')
    (options, args) = parser.parse_args()

    config_dict = {
        'email': options.email,
        'password': options.password
    }

    setup_options = {
        'check': options.check,
        'build': options.build,
        'sdist': options.sdist,
        'install': options.install
    }

    if all(not setup_options[options] for options in setup_options):
        if options.password is None or options.email is None:
            Logger.log("ERROR","You must provide BOTH an E-mail AND password.")
            sys.exit(0)

    count = 0
    for options in setup_options:
        if sum([ count++ setup_options[opts] for opts in setup_options]) == 2:
            Logger.log('ERROR','Only one base options is permitted at a time.')
            sys.exit(0)
        elif setup_options['check']:
            Logger.log("INFO","Grepping System Packages")
            Check().main()
            sys.exit(0)
        elif setup_options['build']: 
            Logger.log('INFO', 'Building setup!')
            break
        elif setup_options['sdist']: 
            Logger.log('INFO', 'Running sdist!')
            break
        elif setup_options['install']: 
            Logger.log('INFO', 'Installing sshmonitorapp.')
            break
        Logger.log('ERROR', 'No base option provided.')
        sys.exit(0)

    prepareBuild = PrepareBuild(setup_options,config_dict)

    Logger.log('INFO','Entering setup in setup.py')

    setup(name='sshmonitor',
    version='1.0.1',
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
        ('/usr/local/bin/', ['src/sshmonitor.py']),
        ('/home/root/.ssh/' ,['src/system/home/user/.ssh/is_sshm_running.sh'])],
    zip_safe=True,
    setup_requires=['python-crontab'],)

    from crontab import CronTab
    prepareBuild.cron_tab()
