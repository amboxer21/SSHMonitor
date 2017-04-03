#/usr/bin/python
# coding: interpy

import smtplib,sys
from optparse import OptionParser

def usage():
    print "Usage: SSHMonitor.py <email address> <password>"
    print "OPTIONS:\n"
    print "    [port]     - If the port is not specified it will default to 445.\n"
    print "    [logging]  - If sshgaurd is installed then you can have SSHGuard log failed and successful\n"
    print "                   attempts. As well as blocked IPs.\n"
    print "    [email]    - This is the email address you want SSHMonitor to send the notifications to.\n"
    print "    [log file] - You can specify the log file or it will default to /var/log/auth.log.\n\n"
    print "SWITCHES:\n"
    print "    Enable SSHGuard logging: --log-enable, -L, log-enable\n"
    print "    Help: --help, -h, help\n"
    print "    Port: --port, -p, port."
    sys.exit(1)

parser = OptionParser()
parser.add_option("-e", "--email", dest='email')
parser.add_option("-p", "--password", dest='password')
(options, args) = parser.parse_args()

if options.email is None:
    print "\nemail cannot be empty!\n"
    usage

if options.password is None:
    print "\nMust provide a password!\n"
    usage

sender  = options.email
to      = sender
message = "Test email"

def send_mail():
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.login(sender,options.password)
        mail.sendmail(sender, to, message)
        print "\nSent email successfully.\n"
    except smtplib.SMTPAuthenticationError:
        print "\nCould not athenticate with password and username!\n"

if len(sys.argv) != 5:
    usage()
else:
    send_mail()
