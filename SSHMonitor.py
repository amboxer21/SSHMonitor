#/usr/bin/python
# coding: interpy

#from pygtail import Pygtail
from tailf import tailf
import smtplib,sys,os,re,time
from optparse import OptionParser

DIRECTORY = '/etc/sshguard'
FAILED = '/etc/sshguard/failed'
SUCCESSFUL = '/etc/sshguard/successful'
BANNED_IPS = '/etc/sshguard/banned_ips'

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

if options.verbose:
    print options

def file_exists(file):
    return os.path.exists(file)

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

for i in [FAILED,SUCCESSFUL,BANNED_IPS]:
    if not file_exists(i):
        open(i, 'w')

def send_mail(sender,to,password,port,subject,body):
    try:
        message = "Subject: {}\n\n{}".format(subject,body)
        mail = smtplib.SMTP('smtp.gmail.com',port)
        mail.starttls()
        mail.login(sender,password)
        mail.sendmail(sender, to, message)
        print "\nSent email successfully.\n"
    except smtplib.SMTPAuthenticationError:
        print "\nCould not athenticate with password and username!\n"

def blocked_ip(title,ip):
    if title == "success":
        w_file = SUCCESSFUL 
    elif title == "failed":
        w_file = FAILED
    elif title == "banned":
        w_file = BANNED_IPS
    else:
        return

    if not options.logdisable:
        print "Using logfile: #{w_file}"
        f = open(w_file, 'a+')
        f.write("#{ip}\n")
        f.close()

def tail_file(logfile):
    for line in tailf(logfile):

        #"Accepted password for nobody from 200.255.100.101 port 58972 ssh2"
        success = re.search("(^.*\d+:\d+:\d+).*sshd.*Accepted password for (.*) from (.*) port.*$", line, re.I | re.M)
        failed  = re.search("(^.*\d+:\d+:\d+).*sshd.*Failed password for.*from (.*) port.*$", line, re.I | re.M)
        blocked = re.search("(^.*\d+:\d+:\d+).*sshguard.*Blocking (.*) for.*$", line, re.I | re.M)

        if success:
            sys.stdout.write("successful - #{success.group(3)}\n")
            blocked_ip("success",success.group(3))
            send_mail(options.email,options.email,options.password,options.port,
                'New SSH Connection', "New ssh connection from #{success.group(3)} for user #{success.group(2)} at #{success.group(1)}")
            time.sleep(1)
        if failed:
            sys.stdout.write("failed - #{failed.group(2)}\n")
            blocked_ip("failed",failed.group(2))
            send_mail(options.email,options.email,options.password,options.port,
                'Failed SSH attempt',"Failed ssh attempt from #{failed.group(2)} at #{failed.group(1)}")
            time.sleep(1)
        if blocked:
            sys.stdout.write("banned - #{blocked.group(2)}\n")
            blocked_ip("banned",blocked.group(2))
            send_mail(options.email,options.email,options.password,options.port,
                'SSH IP Blocked',"#{blocked.group(2)} was banned at #{blocked.group(1)} for too many failed attempts.")
            time.sleep(1)

if len(sys.argv) > 4:
    while True:
        tail_file(options.logfile)

if options.email is None or options.password is None:
    print("\nERROR: Both E-mail and password are required!\n")
    parser.print_help()
