#!/usr/bin/python

import ctypes
from ctypes import cdll

path          = "/home/anthony/Documents/Python/sshmonitor/src/libmasquerade.so"
libmasquerade = cdll.LoadLibrary(path)

libmasquerade.masquerade('anthony','This is a test')
