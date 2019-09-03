# SSHMonitor
**Notice:**
> I USUALLY WORK OFF OF MASTER WITHOUT CREATING NEW BRANCHES(A BAD PRACTICE I KNOW), SO IF YOU CLONE AND DO NOT FORK THEN ANY BUGS YOU ENCOUNTER... YOU ARE ON YOUR OWN.

**About:**
>Monitors incoming ssh requests and will notify you on failed, successful or banned(IP via iptables/sshgaurd) attempts whether they're successful or not. PLEASE FORK INSTEAD OF CLONE THIS REPO. I would greatly appreciate it! Also, you are going to need to setup an outgoing E-mail server in order for the program to work.

This program was written using Python version 2.7 but should work for Python versions 3.x as well.

***

### Build program:

  **[anthony@ghost SSHMonitor]$** `sudo python setup.py install`

^^ NOTE: Check the Crontab and make sure it was actually created.

***

#### You can install sshmonitor via pip as well.

Website:
[https://pypi.org/project/sshmonitor/](https://pypi.org/project/sshmonitor/)

Installation command:
```python
pip install sshmonitor
```

NOTE: Patch is no longer needed for newer versions of python, namely 3.x.x.
