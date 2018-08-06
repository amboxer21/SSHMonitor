#/usr/bin/env python
    
import re
import os
import sys
import time
import logging
import smtplib
import logging.handlers

from tailf import tailf
from optparse import OptionParser

class Logging():

    def __init__(self):
        pass

    def log(self,level,message):
        comm = re.search("(WARN|INFO|ERROR)", str(level), re.M)
        if comm is None:
            print(level + " is not a level. Use: WARN, ERROR, or INFO!")
            return
        try:
            handler = logging.handlers.WatchedFileHandler(
                os.environ.get("LOGFILE","/var/log/sshmonitor.log"))
            formatter = logging.Formatter(logging.BASIC_FORMAT)
            handler.setFormatter(formatter)
            root = logging.getLogger()
            root.setLevel(os.environ.get("LOGLEVEL", str(level)))
            root.addHandler(handler)
            # Log all calls to this class in the logfile no matter what.
            logging.exception("(" + str(level) + ") " + "SSHMonitor - " + str(message))
            # Print to stdout only if the verbose option is passed or log level = ERROR.
            if options.verbose or str(level) == 'ERROR':
                print("(" + str(level) + ") " + "SSHMonitor - " + str(message))
        except Exception as e:
            print("Error in Logging class => " + str(e))
            pass
        return

class FileOpts():

    def __init__(self):
        pass

    def root_directory(self):
        return "/etc/sshguard"

    def failed_path(self):
        return str(self.root_directory()) + '/failed'

    def successful_path(self):
        return str(self.root_directory()) + '/successful'

    def banned_path(self):
        return str(self.root_directory()) + '/banned_ips'

    def current_directory(self):
        return str(os.getcwd())

    def file_exists(self,file_name):
        return os.path.isfile(file_name)

    def create_file(self,file_name):
        if not self.file_exists(file_name):
            open(file_name, 'w')

    def dir_exists(self,dir_path):
        return os.path.isdir(dir_path)

    def mkdir_p(self,dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e:
            if e.errno == errno.EEXIST and self.dir_exists(dir_path):
                pass
            else:
                raise
    
class SSHMonitor():
    
    def __init__(self, config_dict={}):

        self.credential_sanity_check()
        self.logfile_sanity_check(config_dict['logfile'])
        self.display_options()

    def display_options(self):
        verbose = {}
        if config_dict['verbose']:
            for option in config_dict.keys():
                verbose[option] = config_dict[option]
            logger.log("INFO", "Options: " + str(verbose))

    def credential_sanity_check(self):
        if (config_dict['email'] == 'example@gmail.com' or
            config_dict['password'] == 'password'):
                print("\nERROR: Both E-mail and password are required!\n")
                parser.print_help()
                sys.exit(0)

    def logfile_sanity_check(self,logfile):

        log_files = ['messages']

        if os.path.exists(logfile):
            config_dict['logfile'] = logfile
            logger.log("INFO", "logfile(1): " + str(config_dict['logfile']))
        elif logfile == '/var/log/auth.log' and not os.path.exists(logfile):
            for log_file in log_files:
                if os.path.exists('/var/log/' + str(log_file)):
                    config_dict['logfile'] = '/var/log/' + str(log_file)
                    logger.log("INFO", "logfile(2): " + str(config_dict['logfile']))
                    break
                else:
                    logger.log("ERROR","Log file " 
                        + logfile
                        + " does not exist. Please specify which log to use.")
                    sys.exit(0)
    
    def file_exists(self,file):
        return os.path.exists(file)

    def send_mail(self,sender,sendto,password,port,subject,body):
        try:
            message = "Subject: {}\n\n{}".format(subject,body)
            mail = smtplib.SMTP('smtp.gmail.com', port)
            mail.starttls()
            mail.login(sender,password)
            mail.sendmail(sender, sendto, message)
            print("\nSent email successfully.\n")
        except smtplib.SMTPAuthenticationError:
            print("\nCould not athenticate with password and username!\n")
    
    def blocked_ip(self,title,ip,date):
        if title == "success":
            w_file = fileOpts.successful_path() 
        elif title == "failed":
            w_file = fileOpts.failed_path()
        elif title == "banned":
            w_file = fileOpts.banned_path()
        else:
            return
    
        if not config_dict['logdisable']:
            print("Using logfile: " + str(w_file))
            f = open(w_file, 'a+')
            f.write(str(ip) + " - " + str(date) + "\n")
            f.close()
    
    def tail_file(self):
        for line in tailf(config_dict['logfile']):
    
            #"Accepted password for nobody from 200.255.100.101 port 58972 ssh2"
            success = re.search("(^.*\d+:\d+:\d+).*sshd.*Accepted password"
                + " for (.*) from (.*) port.*$", line, re.I | re.M)
            failed  = re.search("(^.*\d+:\d+:\d+).*sshd.*Failed password"
                + " for.*from (.*) port.*$", line, re.I | re.M)
            blocked = re.search("(^.*\d+:\d+:\d+).*sshguard.*Blocking"
                + " (.*) for.*$", line, re.I | re.M)
    
            if success:
                sys.stdout.write("successful - " + success.group(3) + "\n")
                self.blocked_ip("success", success.group(3), success.group(1))
                self.send_mail(config_dict['email'], config_dict['email'],
                    config_dict['password'], config_dict['port'],
                    'New SSH Connection',"New ssh connection from "
                    + success.group(3)
                    + " for user "
                    + success.group(2)
                    + " at "
                    + success.group(1))
                time.sleep(1)
            if failed:
                sys.stdout.write("failed - " + failed.group(2) + "\n")
                self.blocked_ip("failed", failed.group(2), failed.group(1))
                self.send_mail(config_dict['email'],config_dict['email'],
                    config_dict['password'],config_dict['port'],
                    'Failed SSH attempt',"Failed ssh attempt from "
                    + failed.group(2)
                    + " at "
                    + failed.group(1))
                time.sleep(1)
            if blocked:
                sys.stdout.write("banned - " + blocked.group(2) + "\n")
                self.blocked_ip("banned",blocked.group(2),blocked.group(1))
                self.send_mail(config_dict['email'],config_dict['email'],
                    config_dict['password'],config_dict['port'],
                    'SSH IP Blocked', blocked.group(2)
                    + " was banned at "
                    + blocked.group(1)
                    + " for too many failed attempts.")
                time.sleep(1)
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-e", "--email",
        dest='email',
        default='example@gmail.com',
        help='"This argument is required!"')
    parser.add_option("-p", "--password",
        dest='password',
        default='password',
        help='"This argument is required!"')
    parser.add_option("-P", "--port",
        dest='port', type="int",
        default=587,
        help='"Deafults to port 587"')
    parser.add_option("-l", "--log-file",
        dest='logfile',
        default='/var/log/auth.log',
        help='"Defaults to /var/log/auth.log"')
    parser.add_option("-g", "--log-disable",
        dest='logdisable', action="store_true",
        default=False,
        help='"SSHMonitor autologs IPs by default. This turns logging off."')
    parser.add_option("-v", "--verbose",
        dest='verbose', action="store_true",
        default=False,
        help='"Prints args passed to SSHMonitor."')
    (options, args) = parser.parse_args()

    files = [
        'banned_ips',
        'successful',
        'banned']

    config_dict = {
        'email': options.email,
        'password': options.password,
        'port': options.port,
        'logfile': options.logfile,
        'logdisable': options.logdisable,
        'verbose': options.verbose}

    logger   = Logging()
    fileOpts = FileOpts()
    sshm = SSHMonitor(config_dict)

    if not fileOpts.dir_exists(fileOpts.root_directory()):
        fileOpts.mkdir_p(fileOpts.root_directory())
    for f in files:
        if not fileOpts.file_exists(fileOpts.root_directory() + "/" + f): 
            fileOpts.create_file(fileOpts.root_directory() + "/" + f)

    if not fileOpts.file_exists('/var/log/sshmonitor.log'):
        fileOpts.create_file('/var/log/sshmonitor.log')

    if len(sys.argv) > 4:
        while True:
            sshm.tail_file()
