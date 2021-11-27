import os
import time
from datetime import datetime
import web

from switch import Switch


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")


def log_action(operation):
    """Record activity in log file."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")

    # Wait one second to prevent overwriting previous file if it occurred
    # less than one second ago.
    time.sleep(1)
    log_filename = "activity.log"
    full_path = os.path.join(LOG_DIR, log_filename)
    with open(full_path, "a") as log_file:
        log_file.write("[%s] Garage-door operation: %s\n" %
                                                        (timestamp, operation))


# Create objects to represent two controller switches
DoorSwitch = Switch(17) # Uses GPIO17
LightSwitch = Switch(27) # Uses GPIO27

# Mappings of URL to class
urls = (
    '/', 'Main',
    '/light', 'Light'
)

app = web.application(urls, globals())

render = web.template.render('templates/')
# base="layout")

class Main(object):
    def GET(self):
        return render.door_switch_panel()

    def POST(self):
        form = web.input()
        DoorSwitch.short_flip()
        # print('switch flipped')
        log_action("door switch actuated")
        return render.door_switch_panel()


class Light(object):
    def GET(self):
        return render.light_switch_panel()

    def POST(self):
        form = web.input()
        LightSwitch.timed_flip(30*60)
        # print('switch flipped')
        log_action("light switch flipped")
        return render.light_switch_panel()



if __name__ == "__main__":
    app.run()
