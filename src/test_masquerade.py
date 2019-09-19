#!/usr/bin/python

import os
import time

from ctypes import cdll

class TestMasquerade(object):

    def __init__(self,libmasquerade):
        self.libmasquerade = libmasquerade

    def main(self):
        self.libmasquerade.masquerade("anthony", "This is a test.")

if __name__ == '__main__':
    path = "/home/anthony/Documents/Python/sshmonitor/src/tests/libmasquerade2.so"
    test_masquerade = TestMasquerade(cdll.LoadLibrary(path))
    test_masquerade.main()

