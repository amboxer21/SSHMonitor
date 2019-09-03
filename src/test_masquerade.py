#!/usr/bin/python

import ctypes
from ctypes import cdll

path          = "/usr/lib/libmasquerade.so"
libmasquerade = cdll.LoadLibrary(path)

libmasquerade.masquerade('anthony','This is a test')
