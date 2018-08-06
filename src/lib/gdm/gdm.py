#!/usr/bin/env python

import os, re, sys

from subprocess import Popen, call

import src.lib.logging.logger as logger
import src.lib.version.version as version

def add_to_roup(user):
    os.system("sudo usermod -a -G nopasswdlogin " + str(user))

def remove_from_group(user):
    os.system("sudo gpasswd -d " + str(user) + " nopasswdlogin")

def user_present(user):
    with open("/etc/group", "r") as f:
        for line in f:
            nop = re.search("^nopasswdlogin.*(" + str(user) + ")", line)
            if nop is not None and nop:
                return True
            elif nop is not None and not nop:
                return False

def auto_login_remove(auto_login, user):
    if not auto_login and user_present(user):
        remove_from_group(user)

def clear_auto_login(clear, user):
    if len(sys.argv) > 2 and clear:
        logger.log("ERROR", "Too many arguments for clear given. Exiting now.")
        sys.exit(1)
    if clear and user_present(user):
        remove_from_group(user)
        sys.exit(1)
    elif clear and not user_present(user):
        sys.exit(1)

def auto_login(auto_login, user):
    if auto_login:
        logger.log("INFO", "Automatically logging you in now.")
        add_to_roup(user)

def pam_d():
    if version.system_package_manager() == 'rpm':
        return ('password-auth',)
    elif version.system_package_manager() == 'apt':
        return ('common-auth',)
    elif version.system_package_manager() == 'eix':
        return ('system-login',)

