#/usr/bin/python
# coding: interpy
    
import smtplib,sys,os
import re,time,pytailf

from tailf import tailf
from optparse import OptionParser
    
class SSHMonitor():
    
    def __init__(self,
        directory='/etc/sshguard',
        failed='/etc/sshguard/failed',
        successful='/etc/sshguard/successful',
        banned_ips='/etc/sshguard/banned_ips'):

            parser = OptionParser()
            parser.add_option("-e", 
                "--email", dest='email', help='"This argument is required!"')
            parser.add_option("-p",
                "--password", dest='password', help='"This argument is required!"')
            parser.add_option("-P",
                "--port", dest='port', help='"Deafults to port 587"', type="int", default=587)
            parser.add_option("-l",
                "--log-file", dest='logfile', help='"Defaults to /var/log/auth.log"', default='/var/log/auth.log')
            parser.add_option("-g",
                "--log-disable", dest='logdisable', help='"SSHMonitor autologs IPs by default. This turns logging off."', action="store_true",default=False)
            parser.add_option("-v",
                "--verbose", dest='verbose', help='"Prints args passed to SSHMonitor. This is disabled by default."', action="store_true")
            (options, args) = parser.parse_args()

            self.directory  = directory
            self.failed     = failed
            self.successful = successful
            self.banned_ips = banned_ips

            self.logfile    = options.logfile 
            self.email      = options.email
            self.password   = options.password
            self.port       = options.port
            self.logdisable = options.logdisable
    
            if options.verbose:
                print options
    
    def file_exists(self,file):
        return os.path.exists(file)

    def init_files_and_dirs(self):    
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
        for i in [self.failed,self.successful,self.banned_ips]:
            if not self.file_exists(i):
                open(i, 'w')
    
    def send_mail(self,sender,to,password,port,subject,body):
        try:
            message = "Subject: {}\n\n{}".format(subject,body)
            mail = smtplib.SMTP('smtp.gmail.com',port)
            mail.starttls()
            mail.login(sender,password)
            mail.sendmail(sender, to, message)
            print "\nSent email successfully.\n"
        except smtplib.SMTPAuthenticationError:
            print "\nCould not athenticate with password and username!\n"
    
    def blocked_ip(self,title,ip,date):
        if title == "success":
            w_file = self.successful 
        elif title == "failed":
            w_file = self.failed
        elif title == "banned":
            w_file = self.banned_ips
        else:
            return
    
        if not self.logdisable:
            print "Using logfile: #{w_file}"
            f = open(w_file, 'a+')
            f.write("#{ip} - #{date}\n")
            f.close()
    
    def tail_file(self):
        for line in tailf(self.logfile):
    
            #"Accepted password for nobody from 200.255.100.101 port 58972 ssh2"
            success = re.search("(^.*\d+:\d+:\d+).*sshd.*Accepted password for (.*) from (.*) port.*$", line, re.I | re.M)
            failed  = re.search("(^.*\d+:\d+:\d+).*sshd.*Failed password for.*from (.*) port.*$", line, re.I | re.M)
            blocked = re.search("(^.*\d+:\d+:\d+).*sshguard.*Blocking (.*) for.*$", line, re.I | re.M)
    
            if success:
                sys.stdout.write("successful - #{success.group(3)}\n")
                self.blocked_ip("success",success.group(3),success.group(1))
                self.send_mail(self.email,self.email,self.password,self.port,
                    'New SSH Connection', "New ssh connection from #{success.group(3)} for user #{success.group(2)} at #{success.group(1)}")
                time.sleep(1)
            if failed:
                sys.stdout.write("failed - #{failed.group(2)}\n")
                self.blocked_ip("failed",failed.group(2),failed.group(1))
                self.send_mail(self.email,self.email,self.password,self.port,
                    'Failed SSH attempt',"Failed ssh attempt from #{failed.group(2)} at #{failed.group(1)}")
                time.sleep(1)
            if blocked:
                sys.stdout.write("banned - #{blocked.group(2)}\n")
                self.blocked_ip("banned",blocked.group(2),blocked.group(1))
                self.send_mail(self.email,self.email,self.password,self.port,
                    'SSH IP Blocked',"#{blocked.group(2)} was banned at #{blocked.group(1)} for too many failed attempts.")
                time.sleep(1)
    
if __name__ == '__main__':

    sshm = SSHMonitor()
    sshm.init_files_and_dirs()

    if len(sys.argv) > 4:
        while True:
            sshm.tail_file()
    
    if self.email is None or self.password is None:
        print("\nERROR: Both E-mail and password are required!\n")
        parser.print_help()
