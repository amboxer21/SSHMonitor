#!/bin/bash

opt=$1;

declare -a pip=(pytailf interpy)
declare -a deb=(python python-dev python-setuptools python-pip build-essential)
declare -a rpm=(python python-devel python-setuptools python-pip)

function install() {
  manage_pkgs
  if [[ ! -d /home/root/.ssh ]]; then
    sudo mkdir -p /home/root/.ssh/;
  fi
  sudo cp sshmonitor/sshmonitor.py /usr/bin/
  sudo chmod a+x /usr/bin/sshmonitor.py
  sudo cp sshmonitor/build/home/user/.ssh/is_sshm_running.sh /home/root/.ssh/
  sudo sed -i "s/user/$USER/g" sshmonitor/build/root_crontab.txt
  if [[ ! `egrep -io "\*.*is_sshm_running.sh$" /var/spool/cron/crontabs/root` ]]; then
    sudo cat sshmonitor/build/root_crontab.txt >> /var/spool/cron/crontabs/root
  fi
};

function remove() {
  sudo rm /usr/bin/sshmonitor.py 2> /dev/null
  sudo rm /home/root/.ssh/is_sshm_running.sh 2> /dev/null
  sudo sed -i 's/^\*.*.sh$//g' /var/spool/cron/crontabs/root 2> /dev/null
};

function usage() {
  echo -e "-> bash $0 [option]\n\n-> Options: install or remove.\n";
  exit 0;
};

function manage_pkgs() {
  if [[ $pkgm == 'yum' ]]; then
    for y in "${rpm[@]}"; do
      sudo $pkgm -y $opt $y;
    done
  elif [[ $pkgm == 'apt-get' ]]; then
    for d in "${deb[@]}"; do
      sudo apt-get -y $opt $d;
    done
  else
    echo -e "Your package manager is not supported.";
  fi
};

function manage_pip() {
  for p in "${pip[@]}"; do
    case $1 in
      'install')
        if [[ ! `sudo pip --no-cache-dir show $p | awk "/Name: $p/{print $2}"` ]]; then
          sudo pip $opt $p;
        fi
      ;;
      'remove')
        if [[ `sudo pip --no-cache-dir show $p | awk "/Name: $p/{print $2}"` ]]; then
          sudo pip uninstall -y $p;
        fi        
      ;;
    esac
  done
};

if [[ ! $EUID == 0 ]]; then
  echo -e "\nERROR: Must be root!\n";
  exit 0;
fi

for i in apt-get yum; do
  if [[ ! `$i --version 2> /dev/null` == '' ]]; then
    pkgm=$i;
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
  manage_pip 'install';
elif [[ $opt == 'remove' ]]; then
  remove;
  manage_pip 'remove';
else 
  echo -e "\nERROR: $opt is not a valid arg!\n";
  usage;
fi
