#!/usr/bin/env python

import subprocess, re

def name():
    comm = subprocess.Popen(["users"], shell=True, stdout=subprocess.PIPE)
    return re.search("(\w+)", str(comm.stdout.read())).group()
