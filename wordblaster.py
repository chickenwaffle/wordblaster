#!/usr/bin/env monkeyrunner                                                         
#
# This is a Wordscapes bruteforcer for Python 2.5.3
# Version 0.1
#
# Created by Matt Wilson on
# January 5, 2020
#
#
#
# REQUIREMENTS:
#
# - Android SDK
# - Java Development Kit 8
# - Samsung Galaxy S10 (support for more devices to come)
#
#
#
# INSTRUCTIONS:
#
# 1) Connect your phone to your computer via USB cable and ensure that
#    USB debugging is enabled in your phone settings.
#
# 2) Navigate to your platform-tools folder in your Android SDK and run "adb devices"
#    If your device shows up in the list, then your computer recognizes your phone
#    as an Android device.
#
# 3) Navigate to your bin folder in your Android SDK tools
#    e.g. Android/Sdk/tools/bin
#
# 4) Open a SIX CHARACTER Wordscapes level on your phone.
#
# 5) run "monkeyrunner wordblaster.py"
#
#
#
#                     SIX LETTER LAYOUT
#
#                             0
#                        (540, 1500)
#
#
#                5                           1
#           (330, 1620)                 (750, 1620)
#
#
#
#                4                           2
#           (330, 1860)                 (750, 1860)
#
#
#                             3
#                        (540, 1980)
                                                                                    
import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# The lower the number, the faster the lines are drawn.
# Do not go lower than .03
speed = .03

device = MonkeyRunner.waitForConnection()

###################################################################
# 3 LETTER BRUTEFORCER
###################################################################

letters = 3

# The starting point of the line
draw_x = [0,0,0,0,0,0,0,0]
draw_y = [0,0,0,0,0,0,0,0]

filepath = '';
if letters == 3:
    filepath = '/home/matt/code/python3/wordblaster/3letter.txt'
f = open(filepath, "r")

# Read all combinations as strings into an array called 'content'
content = f.readlines()

# Set up the line drawer
for line in content:
    for i in range(1, letters+1):
        pos = i-1

        if int(line[0]) == i:
            draw_x[pos] = 540
            draw_y[pos] = 1500

        elif int(line[1]) == i:
            draw_x[pos] = 750
            draw_y[pos] = 1620

        elif int(line[2]) == i:
            draw_x[pos] = 750
            draw_y[pos] = 1860

        elif int(line[3]) == i:
            draw_x[pos] = 540
            draw_y[pos] = 1980

        elif int(line[4]) == i:
            draw_x[pos] = 330
            draw_y[pos] = 1860

        elif int(line[5]) == i:
            draw_x[pos] = 330
            draw_y[pos] = 1620

    device.touch(draw_x[0], draw_y[0], MonkeyDevice.DOWN)
    time.sleep(speed)
    
    for i in range(1, letters):
        device.touch(draw_x[i], draw_y[i], MonkeyDevice.MOVE)
        time.sleep(speed)

    device.touch(draw_x[letters-1], draw_y[letters-1], MonkeyDevice.UP)

# Delay between words
    time.sleep(.1)
