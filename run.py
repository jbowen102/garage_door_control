from time import sleep
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)

while True:
    switch_pos = input("Type 'on' to switch relay:\n> ")
    if switch_pos == 'on':
        GPIO.output(17, 1)
    sleep(0.2)
    #    for x in range(1000):
    #        pass
    GPIO.output(17, 0)

GPIO.cleanup()


# from wiringPi import *
#
# gpio -g mode 17 out
#
# while True:
#     switch_pos = input("Type 'on' to switch relay:\n> ")
#     if switch_pos == 'on':
#         gpio -g write 17 1
#     # usleep(0.2)
#         for x in range(1000):
#             pass
#     gpio -g write 17 0
