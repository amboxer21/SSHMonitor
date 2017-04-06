#!/bin/bash

if [[ `ps aux | egrep --color -i "root.*[0-9]*:[0-9]* sudo /usr/bin/python /usr/bin/SSHMonitor.py" | wc -l` < 1 ]]; then 
  sudo /usr/bin/python /usr/bin/SSHMonitor.py -e "justdriveapp1@gmail.com" -p "FISH scale 21" & 
fi

if [[ `ps aux | egrep --color -i "root.*[0-9]*:[0-9]* sudo /usr/bin/python /usr/bin/SSHMonitor.py" | wc -l` > 1 ]]; then 
  sudo kill -9 `ps aux | egrep --color -i "root.*[0-9]*:[0-9]* sudo /usr/bin/python /usr/bin/SSHMonitor.py" | awk '{print $2}'`;
fi
