#!/usr/bin/env monkeyrunner
#
# This is a Wordscapes dictionary attacker using Jython 2.5.3
# Version 3.1
#
# Created by Matt Wilson
# January 8, 2020
#
#
#
# REQUIREMENTS:
#
# - Android SDK
# - Java Development Kit 8
# - An Android Phone
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

parser = argparse.ArgumentParser(description='Defeat Wordscapes at its own game')
parser.add_argument('-m', 
                    '--min', 
                    type=int, 
                    default=3, 
                    metavar='', 
                    help='minimum length of words [default=3]')
parser.add_argument('--simulate', 
                    action='store_true',
                    help='Run a simulation without smartphone interaction')
parser.add_argument('letter_bank', 
                    type=str, 
                    default="abcdefg", 
                    help='letters in the circle, starting from the top going clockwise')
parser.add_argument('--slow', action='store_true')
args = parser.parse_args()

if not args.simulate:
    from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

def duplicate (word_builder, found_words):
    if word_builder in found_words:
        #print ("\nFound word: " + word_builder + " (duplicate)")
        return True
    else:
        return False

if __name__ == "__main__":
    # The words found in dictionaries will be stored here
    found_words = []

    # The lower the number, the faster the lines are drawn.
    # Do not go lower than .035
    speed = .035

    circle_size = len(args.letter_bank)

    # Constant coordinates for letters positions in the circle, listed by size
    # TODO: Find some way to un-hardcode this
    CIRCLE5_X = [ 420,  588,  523,  315,  253]
    CIRCLE5_Y = [1656, 1778, 1973, 1973, 1778]

    CIRCLE6_X = [ 417,  581,  581,  417,  257,  257]
    CIRCLE6_Y = [1646, 1740, 1925, 2020, 1925, 1740]

    CIRCLE7_X = [ 420,  575,  612,  506,  335,  228,  266]
    CIRCLE7_Y = [1635, 1710, 1877, 2014, 2014, 1877, 1710]

    if not args.simulate:
        print ("Connecting to Android device... "),
        device = MonkeyRunner.waitForConnection()
        print ("Connected. Running.")

    ###################################################################
    # THE SMARTFORCER
    ###################################################################

    for letters in range (args.min, circle_size+1):

        # These two variables store x,y coordinates for the line drawer.
        # The program will insert values into these arrays after
        #   parsing lines from the loaded drawpath file.
        draw_x = [0,0,0,0,0,0,0]
        draw_y = [0,0,0,0,0,0,0]

        # Load the appropriate file depending on the length of word
        drawpath_file = ''
        dict_file = ''

        if circle_size == 5:
            if letters == 3:
                drawpath_file = 'drawpaths/5circle_3letter.txt'
                dict_file     = 'dictionaries/3dict.txt'
            elif letters == 4:
                drawpath_file = 'drawpaths/5circle_4letter.txt'
                dict_file     = 'dictionaries/4dict.txt'
            elif letters == 5:
                drawpath_file = 'drawpaths/5circle_5letter.txt'
                dict_file     = 'dictionaries/5dict.txt'

        elif circle_size == 6:
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

        elif circle_size == 7:
            if letters == 3:
                drawpath_file = 'drawpaths/7circle_3letter.txt'
                dict_file     = 'dictionaries/3dict.txt'
            elif letters == 4:
                drawpath_file = 'drawpaths/7circle_4letter.txt'
                dict_file     = 'dictionaries/4dict.txt'
            elif letters == 5:
                drawpath_file = 'drawpaths/7circle_5letter.txt'
                dict_file     = 'dictionaries/5dict.txt'
            elif letters == 6:
                drawpath_file = 'drawpaths/7circle_6letter.txt'
                dict_file     = 'dictionaries/6dict.txt'
            elif letters == 7:
                drawpath_file = 'drawpaths/7circle_7letter.txt'
                dict_file     = 'dictionaries/7dict.txt'

        f1 = open(drawpath_file, "r")
        f2 = open(dict_file    , "r")
        
        permutations = f1.readlines()
        dictionary   = f2.readlines()

        # Remove new line characters at the end of each word
        dictionary = [endl.strip() for endl in dictionary]

        # The permutations and dictionary are loaded into memory
        # and we no longer need their file objects.
        f1.close()
        f2.close()

        # For every permutation of length of letters...
        for perm in permutations:
            word_builder = ""

            # For every length of letter chain
            for i in range(1, letters+1):
                pos = i-1

                # For every letter in the circle
                for j in range(0, circle_size):
        
                    # Constructs a readable word from the permutation
                    # if the letters are        'abcdef',
                    # and the permutation is    '210300',
                    # the resulting word is     'bad'   .
                    if int(perm[j]) == i:
                        word_builder += args.letter_bank[j]

                        if circle_size == 5:
                            draw_x[pos] = CIRCLE5_X[j]
                            draw_y[pos] = CIRCLE5_Y[j]
                        elif circle_size == 6:
                            draw_x[pos] = CIRCLE6_X[j]
                            draw_y[pos] = CIRCLE6_Y[j]
                        elif circle_size == 7:
                            draw_x[pos] = CIRCLE7_X[j]
                            draw_y[pos] = CIRCLE7_Y[j]

            # If an actual word is found, store the word in the 
            # array of words, and the permutation in the array
            # of perms
            for dictionary_word in dictionary:

                # When the --slow flag is set, the computer will output what it's comparing
                if args.slow:
                    print ("CPU: \"Is " + word_builder + " the same as " + dictionary_word + "?\"\r"),

                # After the word is found in the dictionary, draw it in the game
                if word_builder == dictionary_word and not duplicate(word_builder, found_words):
                    found_words.append(word_builder)
                    print ("Found word: " + word_builder + "                              ")
                    #time.sleep(1.5) ###########################################################

                    # The pause is to make verbosity easier to read
                    if args.slow:
                        pass
                        #time.sleep(1)

                    # Perform the touch screen interaction here
                    if not args.simulate:
                        device.touch(draw_x[0], draw_y[0], MonkeyDevice.DOWN)
                        time.sleep(speed)
        
                        for i in range(1, letters):
                            device.touch(draw_x[i], draw_y[i], MonkeyDevice.MOVE)
                            time.sleep(speed)
   
                        device.touch(draw_x[letters-1], draw_y[letters-1], MonkeyDevice.UP)
                        if args.slow:
                            time.sleep(speed*6) # Wait a bit longer for animations to stop
                    break

    print ("Done.\n")
