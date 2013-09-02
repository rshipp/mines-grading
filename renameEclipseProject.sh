#!/bin/bash

# renames the proper attr in a .project file to be unique. requires one command
# line arg.  First arg is the unique text the next is the location of the
# .project file

# TODO needs a better way to traverse xml


if [[ ! $# == "2" ]];
then
    exit 1
else
    unique=$1
    dir=$2
fi


sed -i "0,/<name>[^<]*/s//&_$unique/" "$dir"
