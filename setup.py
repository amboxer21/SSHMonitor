#!/usr/bin/env python

import subprocess,re,sys,os,time

import src.lib.gdm.gdm as gdm
import src.lib.logging.logger as logger
import src.lib.version.version as version

from distutils.cmd import Command
from subprocess import Popen, call, PIPE
from setuptools import setup, find_packages
from distutils.errors import DistutilsError, DistutilsExecError

class Check():
    def __init__(self):
        self.sys_dependencies = {
            'rpm': ('python-devel','sqlite3-dbf','syslog-ng','sendmail-cf',
                'sendmail-devel','procmail','opencv-core','opencv-python'),
            'eix': ('mail-mta/sendmail','app-admin/syslog-ng','dev-lang/python',
                'dev-python/sqlite3dbm','mail-filter/procmail','media-libs/opencv'),
            'apt': ('libopencv-dev','python-opencv','python-dev','procmail','sqlite3',
                'sendmail-bin','sendmail-cf','sensible-mda','syslog-ng','sendmail-base')}
        self.package_manager  = {
            'rpm': ('centos','fedora','scientific','opensuse'),
            'apt': ('debian','ubuntu','linuxmint'),
            'eix': ('gentoo',)}

    def system_query_command(self):
        if version.system_package_manager() == 'rpm':
            system_query_command = 'rpm -qa'
        elif version.system_package_manager() == 'apt':
            system_query_command = 'dpkg --list'
        elif version.system_package_manager() == 'eix':
            system_query_command = 'eix -e --only-names'
        return system_query_command

    def grep_system_packages(self,package_name):
        comm = subprocess.Popen([self.system_query_command() + " " + str(package_name)],
            shell=True, stdout=subprocess.PIPE)
        if comm is not None:
            logger.log("INFO", "Package " + str(comm.stdout.read()).strip() + " was found.")
        else:
            logger.log("ERROR", "Package " + str(comm.stdout.read()).strip() + " was not found.")

    def main(self):
        try:
            for item in self.sys_dependencies[version.system_package_manager()]:
                self.grep_system_packages(item)
        except DistutilsExecError as distutilsExecError:
            logger.log("ERROR", "Exception DistutilsExecError: " + str(distutilsExecError))

class PrepareBuild():
    def __init__(self):
        pass

    def cron_tab(self):
        #Count need to be 1 in order to write to the crontab
        #Basically, checking for grep being None or not None will
        # not work in this case and we need to check for 2 occurances.
        count=0
        command="/bin/bash /home/root/.ssh/is_sshm_running.sh"
        cron = CronTab(user='root')
        job = cron.new(command=command)
        job.minute.every(1)
        install = re.search('install', str(sys.argv[1]), re.M | re.I)
        for item in cron:
            grep = re.search(r'\/is_sshm_running.sh', str(item))
            if grep is not None:
                count+=1
        if count < 2 and install is not None:
            logger.log("INFO", "Installing crontab.")
            cron.write()
            print("Please nesure that the crontab was actually installed!")
            print("To do so please run(without quotes) => 'sudo crontab -l -u root'")

if __name__ == '__main__':

    prepareBuild = PrepareBuild()
    argument = re.match(r'(install|check|build|sdist)\b', str(sys.argv[1]))

    if argument is None:
        logger.log("ERROR","Option is not supported.")
        sys.exit(0)
    '''elif argument.group() == 'check':
        logger.log("INFO","Grepping System Packages")
        Check().main()
        sys.exit(0)'''

    logger.log('INFO', 'Entering setup in setup.py')

    setup(name='sshmonitor',
    version='1.0.0',
    url='https://github.com/amboxer21/SSHMonitorPy',
    license='GPL-3.0',
    author='Anthony Guevara',
    author_email='amboxer21@gmail.com',
    description="Monitors incoming ssh requests and will notify you on failed, successful or "
        + "banned(IP via iptables/sshgaurd) attempts whether they're successful or not.",
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
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
        ('/usr/local/bin/', ['src/sshmonitor.py']),
        ('/home/root/.ssh/' ,['src/system/home/user/.ssh/is_sshm_running.sh'])],
    zip_safe=True,
    setup_requires=['pytailf', 'python-crontab'],)

    from crontab import CronTab
    prepareBuild.cron_tab()
