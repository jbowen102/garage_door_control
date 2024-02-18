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
    log_path = os.path.join(LOG_DIR, log_filename)
    # Create log file if it doesn't exist already.
    if not os.path.exists(log_path):
        with open(log_path, "w") as fd:
            pass

    with open(log_path, "a") as log_file:
        log_file.write("[%s] %s by %s.\n" % (timestamp, operation, Source))


class Controller(object):
    def __init__(self):
        # Create objects to represent the controller's two switches
        self.DoorSwitch = Switch(17) # Uses GPIO17
        self.LightSwitch = Switch(27) # Uses GPIO27

        self.bike_lockout_active = False

    def is_bike_lockout_active(self):
        return self.bike_lockout_active

    def enter_bike_lockout(self):
        # Put controller in "bike lockout" state that requires getting out of
        # car before opening door again.
        self.bike_lockout_active = True

    def exit_bike_lockout(self):
        self.bike_lockout_active = False


GarageController = Controller()

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

    def POST(self, lock=False, unlock=False):
        form = web.input()

        if unlock:
            if GarageController.is_bike_lockout_active():
                GarageController.exit_bike_lockout()
                log_action("Garage-door bike lockout deactivated", self)
            else:
                log_action("Garage-door bike lockout inactive already. Redundant deactivation", self)

        if GarageController.is_bike_lockout_active():
            log_action("Garage-door switch actuation FAILED ATTEMPT "
                                                  "(bike lockout active)", self)
        else:
            GarageController.DoorSwitch.short_flip()
            log_action("Garage-door switch actuated", self)

        if lock:
            if GarageController.is_bike_lockout_active():
                log_action("Garage-door bike lockout active already. Redundant activation", self)
            else:
                GarageController.enter_bike_lockout()
                log_action("Garage-door bike lockout activated", self)

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
    def POST(self):
        return super(DoorSCWindshield, self).POST(lock=True)

    def __repr__(self):
        return "Door Switch iOS Shortcut via Biking Windshield Hangtag NFC Scan"

class DoorSCRackTag(Main):
    def POST(self):
        return super(DoorSCRackTag, self).POST(unlock=True)

    def __repr__(self):
        return "Door Switch iOS Shortcut via IS300 Roof Rack AirTag Scan"

class DoorSCBikeTag(Main):
    def POST(self):
        return super(DoorSCBikeTag, self).POST(unlock=True)

    def __repr__(self):
        return "Door Switch iOS Shortcut via Bike AirTag Scan"


class Light(object):
    def GET(self):
        return render.light_switch_panel()

    def POST(self):
        form = web.input()

        minutes = 120
        GarageController.LightSwitch.timed_flip(minutes*60)

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