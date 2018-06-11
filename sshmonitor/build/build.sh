#!/bin/bash

opt=$1;

declare -a deb=(python python-dev python-setuptools python-pip build-essential)
declare -a rpm=(python python-devel python-setuptools python-pip)

if [[ ! `echo $EUID` == 0 ]]; then echo -e "Must be root to run this build script."; exit; fi

function cron_path() {
  path='/var/spool/cron'
  if [[ ! `which crontab 2> /dev/null` ]]; then echo -e "Cron is not installed. Exiting now."; exit; fi
  if [[ -e `$path/crontabs 2> /dev/null` ]]; then 
    cronpath="$path/crontabs";
  elif [[ ! -e `$path/crontabs 2> /dev/null` ]]; then
    cronpath='/var/spool/cron'
  else
    echo -e "Could not find cron path. Please manually add contents of file\n  sshmonitor/build/root_crontab.txt " 
    echo -e "to your crontab. Exiting now.";
    exit;
  fi
};

function install() {
  manage_pkgs
  if [[ ! -d /home/root/.ssh ]]; then
    echo -e "Dir /home/root/.ssh does not exist. Creating it now.\n";
    sudo mkdir -p /home/root/.ssh/;
  fi
  echo -e "\nCopying sshmonitor/sshmonitor.py to /usr/bin/\n";
  sudo cp sshmonitor/sshmonitor.py /usr/bin/
  echo -e "\nChanging permissions on /usr/bin/sshmonitor.py to a+x.\n";
  sudo chmod a+x /usr/bin/sshmonitor.py
  echo -e "\nCopying sshmonitor/build/home/user/.ssh/is_sshm_running.sh to /home/root/.ssh/\n";
  sudo cp sshmonitor/build/home/user/.ssh/is_sshm_running.sh /home/root/.ssh/
  cron_path
  if [[ ! `egrep -io "\*.*is_sshm_running.sh$" $cronpath/root` ]]; then
    echo -e "\nAdding to root crontab.\n";
    sudo cat sshmonitor/build/root_crontab.txt >> $cronpath/root
  fi
  if [[ ! `egrep -io "\*.*is_sshm_running.sh$" $cronpath/root` ]]; then
    echo -e "\n\nCould not install cron. Please manually install and restart the program!\n";
  fi
};

function remove() {
  cron_path
  echo -e "\nRemoving /usr/bin/sshmonitor.py\n";
  sudo rm /usr/bin/sshmonitor.py 2> /dev/null
  echo -e "\nRemoving /home/root/.ssh/is_sshm_running.sh\n";
  sudo rm /home/root/.ssh/is_sshm_running.sh 2> /dev/null
  echo -e "\nEditing crontab $cronpath/root via sed.\n";
  sudo sed -i 's/^\*.*.sh$//g' $cronpath/root 2> /dev/null
  for p in pytailf interpy; do
    if [[ `sudo pip --no-cache-dir show $p | awk "/Name: $p/{print $2}"` ]]; then
      echo -e "\nUninstalling $p pip package.\n";
      sudo pip uninstall -y $p 2> /dev/null;
    fi
  done
};

function usage() {
  echo -e "-> bash $0 [option]\n\n-> Options: install or remove.\n";
  exit 0;
};

function manage_pkgs() {
  if [[ $pkgm == 'yum' ]]; then
    for y in "${rpm[@]}"; do
      echo -e "\n${opt}-ing $opt via $pkgm.\n";
      sudo $pkgm -y $opt $y;
    done
  elif [[ $pkgm == 'apt-get' ]]; then
    for d in "${deb[@]}"; do
      echo -e "\n${opt}-ing $opt via $pkgm.\n";
      sudo $pkgm -y $opt $d;
    done
  else
    echo -e "Your package manager is not supported.";
  fi
};

if [[ ! $EUID == 0 ]]; then
  echo -e "\nERROR: Must be root!\n";
  exit 0;
fi

for i in apt-get yum; do
  if [[ ! `$i --version 2> /dev/null` == '' ]]; then
    pkgm=$i;
    echo -e "\nUsing the $pkgm package manager.\n";
  fi
done

if [[ `egrep -io "\"example@gmail.com\" -p \"password\""  sshmonitor/build/home/user/.ssh/is_sshm_running.sh` ]]; then
  echo -e "\nPlease add your email and password to this file:\nsshmonitor/build/home/user/.ssh/is_sshm_running.sh\n";
  echo -e "Exiting now!\n";
  exit 0;
fi

if [[ $opt == '' ]]; then
  echo -e "\nERROR: Must provide an argument!\n";
  usage;
elif [[ $opt == 'install' ]]; then
  install;
elif [[ $opt == 'remove' ]]; then
  remove;
else 
  echo -e "\nERROR: $opt is not a valid arg!\n";
  usage;
fi
