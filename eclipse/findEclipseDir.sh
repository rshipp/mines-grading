#!/bin/bash

# finds the top level directory of an eclipse project given a directory to
# search through.  If no directory is specified the current directory is used.

if [[ $# == "0" ]];
then
    dir="."
elif [[ $# == "1" ]];
then
    dir=$1
else
    exit 1
fi

find $dir -type f -name ".project" | sed 's/\/.project//'
