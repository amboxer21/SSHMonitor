# SSHMonitor

**Notice:**
>[**OLD**] As of **01-07-2020**, this app no longer runs when using Python3.

>[**OLD**] As of **07-21-2020**, this app is now compatible with Python3. Checkout this branch for use with Python3: https://github.com/amboxer21/SSHMonitor2.7/tree/SSHMonitor3 

>[**LATEST**] As of **07-21-2020**, this app can be used with both Python3 **AND** Python2.

**Important:**
> The notify with ui option is broken with Python3. There seems to be an issue with the **ctypes** system library. See issue [#22](https://github.com/amboxer21/SSHMonitor/issues/22).

**About:**
>SSHMonitor monitors incoming ssh requests and will notify you on failed, successful or banned(IP via iptables/sshgaurd) attempts whether they're successful or not. PLEASE FORK INSTEAD OF CLONE THIS REPO. I would greatly appreciate it! Also, you are going to need to setup an outgoing E-mail server in order for the program to work.


***

### Build program:

  **[anthony@ghost SSHMonitor]$** `sudo python setup.py install`

***

#### You can install sshmonitor via pip as well.

`pip install sshmonitor`

**EDIT:** PIP package has been removed from pypi for now.

Website:
[https://pypi.org/project/sshmonitor/](https://pypi.org/project/sshmonitor/)

Installation command:
```python
pip install sshmonitor
```

***

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

***

#### Compiling

##### Creating libmasquerade shared object WITHOUT pthread

```javascript
gcc -c -fPIC masquerade.c -o masquerade.o
gcc masquerade.o -shared -o libmasquerade.so
```

or 

```javascript
gcc -shared -o libmasquerade.so -fPIC masquerade.c
```

```
anthony@ghost:~/Documents/Python/SSHMonitor2.7/src$ ldd libmasquerade.so
	linux-vdso.so.1 (0x00007fff7a942000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f959891b000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f9598b02000)
anthony@ghost:~/Documents/Python/SSHMonitor2.7/src$
```

##### Creating libmasquerade shared object WITH pthread

```javascript
gcc -c -fPIC masquerade.c -o masquerade.o
gcc masquerade.o -shared -o libmasquerade.so -lpthread
```

or

```javascript
gcc -shared -o libmasquerade.so -fPIC masquerade.c -lpthread
```

```
anthony@ghost:~/Documents/Python/SSHMonitor2.7/src$ ldd libmasquerade.so
	linux-vdso.so.1 (0x00007ffc76d36000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007fa6dcd2a000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fa6dcb69000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fa6dcd71000)
anthony@ghost:~/Documents/Python/SSHMonitor2.7/src$
```

#### Compile GTK UI WITH pthread
```javascript
gcc notify-gtk.c -o notify-gtk `pkg-config --cflags --libs gtk+-2.0` -lpthread
```

or

```javascript
gcc -shared -o libmasquerade.so -fPIC masquerade.c -lpthread
```

#### Compile GTK UI WITHOUT pthread
```javascript
gcc notify-gtk.c -o notify-gtk `pkg-config --cflags --libs gtk+-2.0`
```

or

```javascript
gcc -shared -o libmasquerade.so -fPIC masquerade.c
```

### Testing the UI with Python2.x
```javascript
anthony@ghost:~/Documents/Python/sshmonitor/src$ sudo python
Python 2.7.13 (default, Sep 26 2018, 18:42:22) 
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import os, ctypes
>>> from ctypes import cdll
>>> libmasquerade = cdll.LoadLibrary('/home/anthony/Documents/Python/sshmonitor/src/libmasquerade.so')
>>> libmasquerade.masquerade('anthony')
anthony
```

***

NOTE: Patch is no longer needed for newer versions of python, namely 3.x.x.
