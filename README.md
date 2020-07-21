# SSHMonitor

**PLEASE CHANGE THE E-mail address that the app uses. I am getting E-mails from people using/testing this software.**

**Notice:**
>As of **01-07-2020**, this app no longer runs when using Python3.
>As of **07-21-2020**, this app is now compatible with Python3. Checkout this branch for use with Python3: https://github.com/amboxer21/SSHMonitor2.7/tree/SSHMonitor3 

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

**EDIT:** PIP package has been removed from pypi `for now`.

Website:
[https://pypi.org/project/sshmonitor/](https://pypi.org/project/sshmonitor/)

Installation command:
```python
pip install sshmonitor
```

### Checking out SSHMonitor3 branch

#### If you already have a cloned repo on your localhost
```javascript
anthony@ghost:~/Documents/SSHMonitor2.7$ git branch --track SSHMonitor3 origin/SSHMonitor3
Branch 'SSHMonitor3' set up to track remote branch 'SSHMonitor3' from 'origin'.
anthony@ghost:~/Documents/SSHMonitor2.7$ git checkout SSHMonitor3
Switched to branch 'SSHMonitor3'
Your branch is up to date with 'origin/SSHMonitor3'.
anthony@ghost:~/Documents/SSHMonitor2.7$ git branch
* SSHMonitor3
  master
anthony@ghost:~/Documents/SSHMonitor2.7$ 
```

#### Checking out the SSHMonitor3 branch **ONLY** 

```javascript
anthony@ghost:~/Documents$ git clone git@github.com:amboxer21/SSHMonitor2.7.git -bSSHMonitor3
Cloning into 'SSHMonitor2.7'...
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
remote: Compressing objects: 100% (15/15), done.
remote: Total 1009 (delta 6), reused 1 (delta 0), pack-reused 994
Receiving objects: 100% (1009/1009), 3.76 MiB | 10.79 MiB/s, done.
Resolving deltas: 100% (586/586), done.
anthony@ghost:~/Documents$ cd SSHMonitor2.7/
anthony@ghost:~/Documents/SSHMonitor2.7$ git branch
* SSHMonitor3
anthony@ghost:~/Documents/SSHMonitor2.7$
```

NOTE: Patch is no longer needed for newer versions of python, namely 3.x.x.
