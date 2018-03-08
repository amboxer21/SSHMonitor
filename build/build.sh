#!/bin/bash

sudo apt-get install python python-dev python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install interpy
sudo pip install pytailf
sudo pip install tailf

sudo cp SSHMonitor.py /usr/bin/
sudo chmod a+x /usr/bin/SSHMonitor.py
sudo cp home/user/.ssh/is_sshm_running.sh /home/$USER/.ssh/
sudo sed -i "s/user/$USER/g" root_crontab.txt;
cat root_crontab.txt >> /var/spool/cron/crontabs/root
