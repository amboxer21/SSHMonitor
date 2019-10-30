# SSHMonitor


**Notice:**
> I USUALLY WORK OFF OF MASTER WITHOUT CREATING NEW BRANCHES(**A BAD PRACTICE I KNOW**), SO IF YOU CLONE AND DO NOT FORK THEN ANY BUGS YOU ENCOUNTER... YOU ARE ON YOUR OWN. 

>>Recently I receieved E-mail notifications around 5am from someone using/testing this software. He didn't check/know that this app sends the notifications to **MY** E-mail(sshmonitorapp@gmail.com) which is set in the crontab. Meanwhile he is probably ranting about how much of an idiot I am and how my code base doesn't work. 

>>I work from my laptop which is running Gentoo on i3wm. Sometimes I use my work computer on a lunch break which runs Debian stable. Sometimes things will work on my Gentoo box but will not work on my Debian install. I catch these "cases" when I am working from my work computer.

**Important:**
> The notify with ui option is broken with Python3. Seems to be an issue with the ctypes system library. See issue [#22](https://github.com/amboxer21/SSHMonitor/issues/22).

**About:**
>SSHMonitor monitors incoming ssh requests and will notify you on failed, successful or banned(IP via iptables/sshgaurd) attempts whether they're successful or not. PLEASE FORK INSTEAD OF CLONE THIS REPO. I would greatly appreciate it! Also, you are going to need to setup an outgoing E-mail server in order for the program to work.

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
