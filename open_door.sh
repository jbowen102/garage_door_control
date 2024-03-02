cd /home/user01/garage_door_control

python <<< "import app; app.DoorTerminalAccess('Bash Script \"open_door.sh\"').actuate_door_switch()"

cd - > /dev/null


