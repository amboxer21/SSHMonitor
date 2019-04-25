# SSHMonitor
> Monitors incoming ssh requests and will notify you on failed, successful or banned(IP via iptables/sshgaurd) attempts whether they're successful or not. PLEASE FORK INSTEAD OF CLONE THIS REPO. I would greatly appreciate it! Also, you are going to need to setup an outgoing E-mail server in order for the program to work.

This program was written using Python version 2.7 but I have tried to accommodate Python versions 3.x as well.

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

### Patching Python 3.4

If youre using python 3.4, you might need a patch for the pytailf package. You can find the info [HERE](https://github.com/amboxer21/SSHMonitor/blob/master/src/patches/python3.4/README)
