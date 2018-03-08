#!/bin/bash

opt=$1;

declare -a pip=(pytailf interpy)
declare -a deb=(python python-dev python-setuptools python-pip build-essential)
declare -a rpm=(python python-devel python-setuptools python-pip)

function usage() {
  echo -e "-> bash $0 [option]\n\n-> Options: install or remove.\n";
  exit 0;
};

if [[ ! $EUID == 0 ]]; then
  echo -e "\nERROR: Must be root!\n";
  exit 0;
fi

if [[ $opt == '' ]]; then
  echo -e "\nERROR: Must provide an argument!\n";
  usage;
elif [[ ! $opt == 'install' || ! $opt == 'remove' ]]; then
  echo -e "\nERROR: $opt is not a valid arg!\n";
  usage;
fi

for i in apt-get yum; do
  if [[ ! `$i --version 2> /dev/null` == '' ]]; then
    pkgm=$i;
  fi
done

if [[ $pkgm == 'yum' && $opt == 'install' ]]; then
  for y in "${rpm[@]}"; do
    sudo $pkgm -y $opt $y;
  done 
  finalize;
elif [[ $pkgm == 'apt-get' && $opt == 'install' ]]; then
  for d in "${deb[@]}"; do
    sudo apt-get -y $opt $d;
  done 
  finalize;
elif [[ $opt == 'remove' ]]; then
  remove;
else
  echo -e "Your package manager is not supported.";
fi

for p in "${pip[@]}"; do
  sudo pip $opt $p;
done

function finalize() {
  sudo cp ../sshmonitor/sshmonitor.py /usr/bin/
  sudo chmod a+x /usr/bin/sshmonitor.py
  sudo cp home/user/.ssh/is_sshm_running.sh /home/$USER/.ssh/
  sudo sed -i "s/user/$USER/g" root_crontab.txt
  cat root_crontab.txt >> /var/spool/cron/crontabs/root
};

function remove() {
  sudo rm /usr/bin/sshmonitor.py
  sudo rm /home/$USER/.ssh/is_sshm_running.sh
  sudo sed -i 's/^\*.*.sh$//g' build/root_crontab_bak.txt
};
