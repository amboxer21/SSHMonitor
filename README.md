# SSHMonitor(Python2)


**Notice:**
>As of **01-07-2020**, this app no longer runs when using Python3.

**Important:**
> The notify with ui option is broken with Python3. There seems to be an issue with the **ctypes** system library. See issue [#22](https://github.com/amboxer21/SSHMonitor/issues/22).

**About:**
>SSHMonitor monitors incoming ssh requests and will notify you on failed, successful or banned(IP via iptables/sshgaurd) attempts whether they're successful or not. PLEASE FORK INSTEAD OF CLONE THIS REPO. I would greatly appreciate it! Also, you are going to need to setup an outgoing E-mail server in order for the program to work.


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
