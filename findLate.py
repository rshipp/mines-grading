#!/usr/bin/python
import sys
import os
import re
import time
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
    print "Usage: ./script duedate directory prestring"
    sys.exit(1)
else:
    prestring = sys.argv[3]
    directory = sys.argv[2]
    duedate = time.strptime( sys.argv[1], timeformat )

for each in os.listdir( directory ):
    if isSubmission( each, prestring ):
        usernames[getUsername(each)] = time.strptime( getTime( each,prestring ), timeformat )


print "Late Submissions"
for key in usernames:
    if usernames[key] > duedate:
        dayslate = math.ceil((time.mktime( usernames[ key ] ) - time.mktime( duedate ) ) / float(secs_in_day ))
        print key,": ",time.strftime( timeformat, usernames[key] ),"[",dayslate,"days late]"
