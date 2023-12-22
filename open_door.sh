cd /home/user01/garage_door_control

python <<< "import app; app.DoorSwitch.short_flip()"

python <<< "import app; app.log_action('Garage-door switch actuated', 'Bash Script \"open_door.sh\"')"

cd - > /dev/null


