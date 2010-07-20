'''
Just run this 4 times if you have 4 cpu's. Put the raw files in "../raw" and 
make sure you have a directory called "../resized"
'''

from time import sleep
from random import random

from os import path
from subprocess import call
from glob import glob

SOURCE = "../raw/*.mov"
TARGET_PREFIX = "../resized/r"

MOV_TO_AVI = False
SINGLE_TEST = False

# We'd rather lose 16 pixels of information on the width and gain some more quality with 
# 720x410 instead of 720x402
# we lose roughly 42 pixels from the 1920 pixels wide frame
#CONVERT = "ffmpeg -i %s -s 720x406 -cropbottom 4 -sameq -acodec copy %s"
#CONVERT = "ffmpeg -i %s -s 736x414 -cropbottom 4 -cropright 8 -cropleft 8 -sameq -acodec copy %s"
# the original is 1920x1088 so infact it resizes to 720x408 with 3 bad pixels

# DV-PAL, 720x448, works well. Render to 768x576 in premiere
#CONVERT = "ffmpeg -i %s -s 720x456 -cropbottom 8 -sameq -acodec copy %s"

# DV-PAL, works  better
#CONVERT = "ffmpeg -i %s -s 768x458 -cropbottom 8 -sameq -acodec copy %s"

# DV-PAL, works  better
CONVERT = "ffmpeg -i %s -s 768x440 -cropbottom 8 -sameq -acodec copy %s"

# 720p is 1270x720, need to remove 8 pixels to make the crop work.
#CONVERT = "ffmpeg -i %s -s 1280x728 -cropbottom 8 -sameq -acodec copy %s"

EXTRACT = "ffmpeg -i %s -acodec copy %s"
# remix sound back in
# ffmpeg -i rMVI_7012.MOV -i LS100217-w.wav -map 0:0 -map 1:0 -vcodec copy -acodec copy new.mov

# 3 to 2 fix
if not hasattr(__builtins__, 'raw_input'):
    raw_input = input

def RandomDelay():
    """
    sleep random amount (0 - 1 seconds) so that race conditions are less likely
    in case of running a few of these atthe same time.
    """
    sleep(random())
    

def GetTargetName(sourcename):
    targetname = TARGET_PREFIX + path.basename(sourcename)
    
    if MOV_TO_AVI:
        targetname = targetname.replace('.MOV', '.avi')
    
    return targetname

def Convert(source, target):
    convert_cmd = CONVERT % (source, target)
    return call(convert_cmd)

def ExtractWav(source, target):
    target = target + '.wav'
    extract_cmd = EXTRACT % (source, target)
    return call(extract_cmd)

def Run(function, src, dst):
    ret_val = function(src, dst)
    print("%s returned: %d" % (function.__name__, ret_val))
    if 0 != ret_val:
        raw_input("Perhaps an error occurred, press enter to continue")
    
def Main():
    files = glob(SOURCE)
    print files
    for src in files:
        dst = GetTargetName(src)
        if path.isfile(dst):
            print "target exists, skipping %s" % dst
        else:
            # target file doesn't exist yet, run the conversion
            Run(Convert, src, dst)
            
            Run(ExtractWav, src, dst)


if __name__ == "__main__":
    RandomDelay()
    if SINGLE_TEST:
        Run(Convert, '../raw/MVI_8981.MOV', 'rMVI_8981.mov')
    else:
        Main()


