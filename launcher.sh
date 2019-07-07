#!/bin/sh
# launcher.#!/bin/sh
# navigate to root directory, then to this directory, then execute python script, then back to root

cd /
cd ~/garage_door_control
sudo python app.py
cd /


# added this to root crontab (using command 'sudo crontab -e':
# @reboot sh ~/garage_door_control/launcher.sh > ~/garage_door_control/logs/cronlog 2>&1
