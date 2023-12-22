import os
import time
from datetime import datetime
import web

import RPi.GPIO as GPIO

from switch import Switch


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")


def log_action(operation, Source):
    """Record activity in log file."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")

    # Wait one second to prevent overwriting previous file if it occurred
    # less than one second ago.
    time.sleep(1)
    log_filename = "activity.log"
    full_path = os.path.join(LOG_DIR, log_filename)
    with open(full_path, "a") as log_file:
        log_file.write("[%s] %s by %s.\n" % (timestamp, operation, Source))


# Create objects to represent two controller switches
DoorSwitch = Switch(17) # Uses GPIO17
LightSwitch = Switch(27) # Uses GPIO27

# Mappings of URL to class
urls = (
    '/', 'Main',
    '/SC', 'DoorSC',
    '/SC-Badge', 'DoorSCBadge',
    '/SC-Windshield', 'DoorSCWindshield',
    '/SC-RackTag', 'DoorSCRackTag',
    '/SC-BikeTag', 'DoorSCBikeTag',
    '/light', 'Light',
    '/light-shortcut', 'LightSC'
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

        log_action("Garage-door switch actuated", self)
        return render.door_switch_panel()

    def __repr__(self):
        return "Webpage Door Switch"

class DoorSC(Main):
    def __repr__(self):
        return "Door Switch iOS Shortcut"

class DoorSCBadge(Main):
    def __repr__(self):
        return "Door Switch iOS Shortcut via Badge NFC Scan"

class DoorSCWindshield(Main):
    def __repr__(self):
        return "Door Switch iOS Shortcut via Biking Windshield Hangtag NFC Scan"

class DoorSCRackTag(Main):
    def __repr__(self):
        return "Door Switch iOS Shortcut via IS300 Roof Rack AirTag Scan"

class DoorSCBikeTag(Main):
    def __repr__(self):
        return "Door Switch iOS Shortcut via Bike AirTag Scan"


class Light(object):
    def GET(self):
        return render.light_switch_panel()

    def POST(self):
        form = web.input()

        minutes = 120
        LightSwitch.timed_flip(minutes*60)

        log_action("Light switch flipped", self)
        return render.light_switch_panel()

    def __repr__(self):
        return "Light Switch Webpage"

class LightSC(Light):
    def __repr__(self):
        return "Light Switch iOS Shortcut"



if __name__ == "__main__":
    app.run()
    GPIO.cleanup()