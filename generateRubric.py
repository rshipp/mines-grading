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
    print("""\
Usage: ./script <rubric> <directory> <prestring>
------
Rubric    : path to a given file to be copied for each user
Directory : place where unzip.py was run and containing all the user submissions
Prestring : The text before the username in each user submission

For the given rubric copy it for each user submission found in the given
directory as dictacted by the standard blackboard regex. 
    i.e. prestring_username_attempt_date_filename. 
Multiple user submissions are ignored.


Example:
    Given that you have run unzip.py on the following file:
        gradebook_spring2013-CSCI306A_FProj-Pgm.zip
    You can now run:

    ./script Rubric.txt . FProg-Pgm 
""")
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
