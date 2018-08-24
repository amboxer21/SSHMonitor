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
        try:
            handler = logging.handlers.WatchedFileHandler(
                os.environ.get("LOGFILE","/var/log/sshmonitor.log"))
            formatter = logging.Formatter(logging.BASIC_FORMAT)
            handler.setFormatter(formatter)
            root = logging.getLogger()
            root.setLevel(os.environ.get("LOGLEVEL", str(level)))
            root.addHandler(handler)
            if comm is None:
                print(level + " is not a level. Use: WARN, ERROR, or INFO!")
                return
            elif comm.group() == 'ERROR':
                logging.error("(" + str(level) + ") " + "SSHMonitor - " + str(message))
            elif comm.group() == 'INFO':
                logging.info("(" + str(level) + ") " + "SSHMonitor - " + str(message))
            elif comm.group() == 'WARN':
                logging.warn("(" + str(level) + ") " + "SSHMonitor - " + str(message))
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
        logger.log("INFO", "File " + str(file_name) + " exists.")
        if not self.file_exists(file_name):
            logger.log("INFO", "Creating file " + str(file_name) + ".")
            open(file_name, 'w')

    def dir_exists(self,dir_path):
        return os.path.isdir(dir_path)

    def mkdir_p(self,dir_path):
        try:
            logger.log("INFO", "Creating directory " + str(dir_path))
            os.makedirs(dir_path)
        except OSError as e:
            if e.errno == errno.EEXIST and self.dir_exists(dir_path):
                pass
            else:
                logger.log("ERROR", "mkdir error: " + str(e))
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
                logger.log("ERROR", "Both E-mail and password are required!")
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
    
    def send_mail(self,sender,sendto,password,port,subject,body):
        try:
            message = "Subject: {}\n\n{}".format(subject,body)
            mail = smtplib.SMTP('smtp.gmail.com', port)
            mail.starttls()
            mail.login(sender,password)
            mail.sendmail(sender, sendto, message)
            logger.log("INFO", "Sent email successfully.")
        except smtplib.SMTPAuthenticationError:
            logger.log("ERROR", "Could not athenticate with password and username!")
    
    def log_attempt(self,title,ip,date):
        if title == "success":
            w_file = fileOpts.successful_path() 
        elif title == "failed":
            w_file = fileOpts.failed_path()
        elif title == "banned":
            w_file = fileOpts.banned_path()
        else:
            logger.log("WARN", str(title) + " is not a known title name/type.")
            return
    
        if config_dict['logdisable']:
            logger.log("INFO", "Logging SSH attempts have been disabled.")
            return
        logger.log("INFO", "Logging SSH actions to file: " + str(w_file))
        f = open(w_file, 'a+')
        f.write(str(ip) + " - " + str(date) + "\n")
        f.close()
    
    def tail_file(self, logfile):
        for line in tailf(config_dict['logfile']):
    
            #"Accepted password for nobody from 200.255.100.101 port 58972 ssh2"
            success = re.search("(^.*\d+:\d+:\d+).*sshd.*Accepted password"
                + " for (.*) from (.*) port.*$", line, re.I | re.M)
            failed  = re.search("(^.*\d+:\d+:\d+).*sshd.*Failed password"
                + " for.*from (.*) port.*$", line, re.I | re.M)
            blocked = re.search("(^.*\d+:\d+:\d+).*sshguard.*Blocking"
                + " (.*) for.*$", line, re.I | re.M)
    
            if success:
                logger.log("INFO", "Successful SSH login from " + success.group(3))
                self.log_attempt("success", success.group(3), success.group(1))
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
                logger.log("INFO", "Failed SSH login from " + failed.group(2))
                self.log_attempt("failed", failed.group(2), failed.group(1))
                self.send_mail(config_dict['email'],config_dict['email'],
                    config_dict['password'],config_dict['port'],
                    'Failed SSH attempt',"Failed ssh attempt from "
                    + failed.group(2)
                    + " at "
                    + failed.group(1))
                time.sleep(1)
            if blocked:
                logger.log("INFO", "IP address " + blocked.group(2) + " was banned!")
                self.log_attempt("banned",blocked.group(2),blocked.group(1))
                self.send_mail(config_dict['email'],config_dict['email'],
                    config_dict['password'],config_dict['port'],
                    'SSH IP Blocked', blocked.group(2)
                    + " was banned at "
                    + blocked.group(1)
                    + " for too many failed attempts.")
                time.sleep(1)

    def main(self):

        _version_ = re.search('\d\.\d\.\d{1,2}', str(sys.version))

        logger.log("INFO", "Python version set to " + str(_version_.group()) + ".")

        while True:
            try:
                self.tail_file(config_dict['logfile'])
            except IOError as ioError:
                logger.log("ERROR", "IOError: " + str(ioError))
            except KeyboardInterrupt:
                logger.log("INFO", " [Control C caught] - Exiting ImageCapturePy now!")
                break

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

    if not fileOpts.dir_exists(fileOpts.root_directory()):
        fileOpts.mkdir_p(fileOpts.root_directory())
    for f in files:
        if not fileOpts.file_exists(fileOpts.root_directory() + "/" + f): 
            fileOpts.create_file(fileOpts.root_directory() + "/" + f)

    if not fileOpts.file_exists('/var/log/sshmonitor.log'):
        fileOpts.create_file('/var/log/sshmonitor.log')

    SSHMonitor(config_dict).main()
