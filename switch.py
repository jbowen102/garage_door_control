import time
import datetime as dt
import os
import signal

import RPi.GPIO as GPIO


class Switch(object):
    def __init__(self, gpio_num):
        self.gpio_num = gpio_num
        self.time_on = False

    def short_flip(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.OUT)

        GPIO.output(self.gpio_num, 1)
        time.sleep(0.2)
        GPIO.output(self.gpio_num, 0)


    def timed_flip(self, timeout):
        """Turns a switch on for set amount of time or turns switch off.
        Timeout measured in seconds
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_num, GPIO.OUT)

        if self.time_on and self.on_time_elapsed() >= dt.timedelta(seconds=timeout):
	    # Since child process can't modify attribute, self.time_on can
	    # be True after countdown already over. Manually set it off here.
	    self.time_on = False

        # If light is already on, turn off and terminate existing countdown.
        if self.time_on:
            # print("%d: TIMER on already" % os.getpid()) # DEBUG
            os.kill(self.pid, signal.SIGINT)
            self.time_on = False
            # print("%d: TIMER turned off" % os.getpid()) # DEBUG
            GPIO.output(self.gpio_num, 0)
            # print("%d: LIGHT turned off" % os.getpid()) # DEBUG

        else:
            GPIO.output(self.gpio_num, 1)
            # print("%d: LIGHT turned on" % os.getpid()) # DEBUG

            self.pid = os.fork()
            if self.pid: # parent process
                self.time_on = dt.datetime.now()
                # print("%d: TIMER turned on" % os.getpid()) # DEBUG
            else: # child process
                # turn light off after timeout
                time.sleep(timeout)
                GPIO.output(self.gpio_num, 0)
                # print("%d: LIGHT turned off" % os.getpid()) # DEBUG
                self.time_on = False # doesn't work
                # print("%d: TIMER turned off" % os.getpid()) # DEBUG

    def on_time_elapsed(self):
        """Evaluates time elapsed since timed_flip() turned on.
        Returns value in seconds.
        """
        # https://www.tutorialspoint.com/How-can-we-do-date-and-time-math-in-Python
	if not self.time_on:
            return False
	else:
	    time_now = dt.datetime.now()
	    return time_now - self.time_on
