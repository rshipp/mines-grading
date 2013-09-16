#!/usr/bin/python
import sys
import os
import re
import shutil
from zipfile import * 
import subprocess

usernames = dict()

# TODO
  # case when user submits extra files in their submission.  These files should
  # be wrapped into their directory.

if len(sys.argv) != 3:
    print("""Please give me a directory and the string to remove before the
    username (without underscore)""")
    sys.exit(1)
else:
    directory = sys.argv[1]
    prestring = sys.argv[2]


for each in os.listdir( directory ):
    if re.match(".*.zip", each ):
        contents = each.split("_")
        if contents[0] == prestring :
            current = 1
            while contents[1] + str(current) in usernames:
                current += 1
            studentdirectory = contents[1] + str(current)
            usernames[studentdirectory] = ""
            # make directory with the current
            os.mkdir( os.path.join( directory, studentdirectory) )
            # unzip to that directory
            print("unzip:", os.path.join( directory, each ))
            print("to:", os.path.join( directory, studentdirectory))

            try:
                with ZipFile( os.path.join( directory, each), 'r') as toUnzip:
                    toUnzip.debug = 3
                    toUnzip.extractall( os.path.join( directory, studentdirectory))
                    if ( not toUnzip ) :
                        print("error")
            except BadZipfile:
                print("Bad zip file")
