#!/bin/bash

declare -a pip=(pytailf interpy)
declare -a deb=(python python-dev python-setuptools python-pip build-essential)
declare -a rpm=(python python-devel python-setuptools python-pip)

for i in apt-get apt yum dnf; do
  if [[ ! `$i --version 2> /dev/null` == '' ]]; then
    pkgm=$i;
  fi
done

if [[ $pkgm == 'yum' || pkgm == 'dnf' ]]; then
  for y in "${rpm[@]}"; do
    sudo $pkgm -y install $y;
  done 
elif [[ $pkgm == 'apt' || $pkgm == 'apt-get' ]]; then
  for d in "${deb[@]}"; do
    sudo apt-get -y install $d;
  done 
else
  echo -e "Your package manager is not supported.";
fi

for p in "${pip[@]}"; do
  sudo pip install $p;
done

sudo cp ../SSHMonitor.py /usr/bin/
sudo chmod a+x /usr/bin/SSHMonitor.py
sudo cp home/user/.ssh/is_sshm_running.sh /home/$USER/.ssh/
sudo sed -i "s/user/$USER/g" root_crontab.txt
cat root_crontab.txt >> /var/spool/cron/crontabs/root
