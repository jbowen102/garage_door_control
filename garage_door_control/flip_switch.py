from time import sleep
import RPi.GPIO as GPIO


def flip():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.OUT)

    GPIO.output(17, 1)
    sleep(0.2)
    GPIO.output(17, 0)

    GPIO.cleanup()



## Original standalone terminal-query version
# from time import sleep
# import RPi.GPIO as GPIO
#
#
# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(17, GPIO.OUT)

# while True:
#     switch_pos = input("Type 'on' to switch relay:\n> ")
#     if switch_pos == 'on':
#         GPIO.output(17, 1)
#     sleep(0.2)
#
#     GPIO.output(17, 0)
#
# GPIO.cleanup()
