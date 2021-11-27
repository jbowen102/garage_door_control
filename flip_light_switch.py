import time
import os
import RPi.GPIO as GPIO


def flip():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(27, GPIO.OUT)

    GPIO.output(27, 1)

    timeout = 30*60
    pid = os.fork()

    if pid: # parent process
        pass
    else: # child process
        # turn light off after 30 minutes
        time.sleep(timeout)
        GPIO.output(27, 0)
        # GPIO.cleanup()
