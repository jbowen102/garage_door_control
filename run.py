import RPi.GPIO as GPIO

GPIO.setup(17, GPIO.OUT)

while True:
    switch_pos = input("Type 'on' to switch relay:\n> ")
    if switch_pos == 'on':
        GPIO.output(17, HIGH)
    # usleep(0.2)
        for x in range(1000):
            pass
    GPIO.output(17, LOW)

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
