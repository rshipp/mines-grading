#!/usr/bin/python
import sys
import os
import re
import shutil
import math

regex = "_([^_]*)_attempt_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})(_[^\.]*)?\..*"

def isSubmission( string, projectName ):
    return re.match(projectName + regex, string)

def getUsername( string ):
    return string.split("_")[1]

def getTime( string, projectName ):
    return re.match( projectName + regex, string ).group(2)


usernames = dict()

timeformat = "%Y-%m-%d-%H-%M-%S"
secs_in_day = 86400

if not len(sys.argv) == 4:
    print "Usage: ./script rubric directory prestring"
    sys.exit(1)
else:
    prestring = sys.argv[3]
    directory = sys.argv[2]
    rubric = sys.argv[1]

for each in os.listdir( directory ):
    if isSubmission( each, prestring ):
        usernames[getUsername(each)] = ""

for key in usernames:
    shutil.copy(rubric, os.path.join(directory,key + ".txt"))
