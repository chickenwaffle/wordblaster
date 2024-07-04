#!/usr/bin/env monkeyrunner
#
# This is a dictionary attacker for Wordscapes-style Android games using Jython 2.5.3
# Version 3.1
#
# Created by Matt Wilson
# January 8, 2020
#
#
#
# REQUIREMENTS:
#
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
#                        Galaxy S10
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
parser.add_argument('-o', 
                    '--only', 
                    type=int, 
                    default=-1, 
                    metavar='', 
                    help='only solve words of this length [default=3]')
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

# Drawpath files are stored in drawpaths/
# If given the function is     get_drawpath_file(5,3)
# then the result is           return "drawpaths/5circle_3letter.txt"
def get_drawpath_file(circle_size, letters):
    return "drawpaths/" + str(circle_size) + "circle_" + str(letters) + "letter.txt"

# Returns a set containing a hash map of every line in a file
# Used for obtaining O(1) search complexity
def load_words(file_path):
    words = set()

    f = open(file_path, "r") 

    dictionary   = f.readlines()

    # Remove new line characters at the end of each word
    dictionary = [endl.strip() for endl in dictionary]

    for word in dictionary:
        words.add(word)

    return words

if __name__ == "__main__":
    # The words found in dictionaries will be stored here
    found_words = set()

    # The lower the number, the faster the lines are drawn.
    # Milliseconds to sleep in between touch events (down,drag,release)
    # Do not go lower than .035
    speed = .04

    circle_size = len(args.letter_bank)

    # Constant coordinates for letters positions in the circle, listed by size
    # TODO: Find some way to un-hardcode this

    if circle_size is 3:
        CIRCLE5_X = [ 540,  588,  523]
        CIRCLE5_Y = [1585, 1778, 1973]

    if circle_size is 4:
        CIRCLE5_X = [ 540,  588,  523,  315]
        CIRCLE5_Y = [1585, 1778, 1973, 1973]

    if circle_size is 5:
        CIRCLE5_X = [ 540,  768,  682,  400,  312]
        CIRCLE5_Y = [1585, 1750, 2018, 2018, 1750]

    elif circle_size is 6:
        CIRCLE6_X = [ 540,  581,  581,  417,  257,  257]
        CIRCLE6_Y = [1585, 1750, 2018, 2018, 1750, 1740]

    elif circle_size is 7:
        CIRCLE7_X = [ 540,  737,  783,  648,  432,  295,  344]
        CIRCLE7_Y = [1585, 1664, 1874, 2044, 2044, 1874, 1664]

    if not args.simulate:
        print ("Connecting to Android device... "),
        device = MonkeyRunner.waitForConnection()
        print ("Connected.")



    ###################################################################
    # THE DICTIONARY ATTACK
    ###################################################################

    min_wordlength = args.min
    max_wordlength = circle_size + 1
    
    # Jank, but if --only is specified, only solve for x length words
    # then stop running
    if args.only > 0:
        min_wordlength = args.only
        max_wordlength = args.only + 1 # has to be higher than min or the script won't run

    for letters in range (min_wordlength, max_wordlength):

        # These two variables store x,y coordinates for the line drawer.
        # The program will insert values into these arrays after
        #   parsing lines from the loaded drawpath file.
        draw_x = [0,0,0,0,0,0,0]
        draw_y = [0,0,0,0,0,0,0]

        # Load the appropriate file depending on the length of word
        # and amount of letters in the circle
        f = open(get_drawpath_file(circle_size, letters), "r")
        permutations = f.readlines()
        f.close()

        dictionary = load_words("dictionary.txt")

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

                        if circle_size == 3:
                            draw_x[pos] = CIRCLE3_X[j]
                            draw_y[pos] = CIRCLE3_Y[j]
                        elif circle_size == 4:
                            draw_x[pos] = CIRCLE4_X[j]
                            draw_y[pos] = CIRCLE4_Y[j]
                        elif circle_size == 5:
                            draw_x[pos] = CIRCLE5_X[j]
                            draw_y[pos] = CIRCLE5_Y[j]
                        elif circle_size == 6:
                            draw_x[pos] = CIRCLE6_X[j]
                            draw_y[pos] = CIRCLE6_Y[j]
                        elif circle_size == 7:
                            draw_x[pos] = CIRCLE7_X[j]
                            draw_y[pos] = CIRCLE7_Y[j]

                    
            # After the word is found in the dictionary, draw it in the game
            if word_builder in dictionary and word_builder not in found_words:

                # Add word to a list of already discovered words to save time
                found_words.add(word_builder) 

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
                    device.touch(draw_x[letters-1], draw_y[letters-1], MonkeyDevice.UP)
                    time.sleep(speed)

    print ("Done.\n")
