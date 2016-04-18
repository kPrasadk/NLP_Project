#!/bin/sh

echo "START " > temp.txt 
cat $1 >> temp.txt
 cat temp.txt |perl -pe 's/[ ]+/ /g and s/[\n]/STOP\nSTART/g' | sed \$d  > $1
 rm temp.txt
