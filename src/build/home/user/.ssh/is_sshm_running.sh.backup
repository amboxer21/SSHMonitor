#!/bin/bash

if [[ `ps aux | egrep --color -i "root.*[0-9]*:[0-9]* sudo /usr/bin/python /usr/bin/sshmonitor.py" | wc -l` < 1 ]]; then 
  sudo /usr/bin/python /usr/bin/sshmonitor.py -e "example@gmail.com" -p "password" & 
fi

if [[ `ps aux | egrep --color -i "root.*[0-9]*:[0-9]* sudo /usr/bin/python /usr/bin/sshmonitor.py" | wc -l` > 1 ]]; then 
  sudo kill -9 `ps aux | egrep --color -i "root.*[0-9]*:[0-9]* sudo /usr/bin/python /usr/bin/sshmonitor.py" | awk '{print $2}'`;
fi
