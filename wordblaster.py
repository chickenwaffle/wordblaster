#!/usr/bin/env monkeyrunner                                                         
#
# This is a Wordscapes bruteforcer for Jython 2.5.3
# Version 1.4
#
# Created by Matt Wilson
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
#    in a terminal. If your device shows up in the list, then your computer 
#    recognizes your phone as an Android device.
#
# 3) Navigate to your bin folder in your Android SDK tools
#    e.g. Android/Sdk/tools/bin
#
# 4) Open a Wordscapes level on your phone.
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
import argparse
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

parser = argparse.ArgumentParser(description='Defeat Wordscapes at its own game')
parser.add_argument('-c', \
                    '--circle_size', \
                    type=int, \
                    default=6, \
                    metavar='', \
                    help='Number of letters in circle [default=6]')
parser.add_argument('-m', \
                    '--min', \
                    type=int, \
                    default=3, \
                    metavar='', \
                    help='length of words to start bruteforcing [default=3]')
parser.add_argument('letter_bank', \
                    type=str, \
                    default="abcdefg", \
                    metavar='', \
                    help='letters in the circle, starting from the top going clockwise')
args = parser.parse_args()



if __name__ == "__main__":
    # The words found in dictionaries will be stored here
    #found_words = []
    found_perms = []
    # The lower the number, the faster the lines are drawn.
    # Do not go lower than .03
    speed = .06

    # Constant coordinates for letters positions in the circle, listed by size
    CIRCLE6_X = [ 540,  750,  750,  540,  330, 330 ]
    CIRCLE6_Y = [1500, 1620, 1860, 1980, 1860, 1620]

    device = MonkeyRunner.waitForConnection()

    ###################################################################
    # THE BRUTEFORCER
    ###################################################################

    for letters in range (args.min, args.circle_size+1):

        # These two variables store x,y coordinates for the line drawer.
        # The program will insert values into these arrays after
        #   parsing lines from the loaded drawpath file.
        draw_x = [0,0,0,0,0,0,0]
        draw_y = [0,0,0,0,0,0,0]

        # Load the appropriate file depending on the length of word
        drawpath_file = ''
        dict_file = ''

        if letters == 3:
            drawpath_file = 'drawpaths/6circle_3letter.txt'
            dict_file     = 'dictionaries/3dict.txt'
        elif letters == 4:
            drawpath_file = 'drawpaths/6circle_4letter.txt'
            dict_file     = 'dictionaries/4dict.txt'
        elif letters == 5:
            drawpath_file = 'drawpaths/6circle_5letter.txt'
            dict_file     = 'dictionaries/5dict.txt'
        elif letters == 6:
            drawpath_file = 'drawpaths/6circle_6letter.txt'
            dict_file     = 'dictionaries/6dict.txt'
        f1 = open(drawpath_file, "r")
        f2 = open(dict_file    , "r")
        
        permutations = f1.readlines()
        dictionary   = f2.readlines()

        # Remove new line characters at the end of each word
        dictionary = [endl.strip() for endl in dictionary]

        f1.close()
        f2.close()

        # For every permutation of length of letters...
        for perm in permutations:
            stringbuilder = ""

            # For every length of letter chain
            for i in range(1, letters+1):
                pos = i-1

                # For every letter in the circle
                for j in range(0, args.circle_size):
        
                    # Constructs a readable word from the permutation
                    # if the letters are        'abcdef',
                    # and the permutation is    '210300',
                    # the resulting word is     'bad'   .
                    if int(perm[j]) == i:
                        stringbuilder += args.letter_bank[j]

                        draw_x[pos] = CIRCLE6_X[j]  # TODO: Rewrite a way to
                        draw_y[pos] = CIRCLE6_Y[j]  # TODO: work with smaller/bigger circles

            # If an actual word is found, store the word in the 
            # array of words, and the permutation in the array
            # of perms
            for word in dictionary:
                if stringbuilder == word:
                    print ("Word found: " + stringbuilder)

                    # Perform the touch screen interaction here
                    device.touch(draw_x[0], draw_y[0], MonkeyDevice.DOWN)
                    time.sleep(speed)
        
                    for i in range(1, letters):
                        device.touch(draw_x[i], draw_y[i], MonkeyDevice.MOVE)
                        time.sleep(speed)
   
                    device.touch(draw_x[letters-1], draw_y[letters-1], MonkeyDevice.UP)
                    time.sleep(speed)

                    time.sleep(speed*5)
