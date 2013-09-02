#!/bin/bash

# arg1 : directory where students projects are

IFS=$'\n' # to deal with those silly people who put spaces in their project file names
list=`findEclipseDir.sh $1`

for each in $list
do
    name="(`echo "$each" | sed 's/\.\/\([^\/]*\)\(\/.*\)\?/\1/'`)"
    file="$each/.project"
    renameEclipseProject.sh "$name" "$file"
    echo "name=$name"
    echo "file=$file"
done

