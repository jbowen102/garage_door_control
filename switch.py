import time
import os
import RPi.GPIO as GPIO


class Switch(object):
    def __init__(self, gpio_num):
        self.gpio_num = gpio_num
        self.timer_on = False

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

        # If light is already on, turn off and terminate existing countdown.
        if self.timer_on:
            os.kill(self.pid, signal.SIGINT)
            self.timer_on = False
            GPIO.output(self.gpio_num, 0)

        else:
            GPIO.output(self.gpio_num, 1)

            self.pid = os.fork()
            if self.pid: # parent process
                self.timer_on = True
            else: # child process
                # turn light off after timeout
                time.sleep(timeout)
                GPIO.output(self.gpio_num, 0)
                self.timer_on = False
