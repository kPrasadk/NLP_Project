#!/bin/bash

#cat $@ | tr ' ' '\n' | sort | uniq -c | awk '{
#		if ( $1 > 1 ) 
#			 print $2 ;
#		}' > vocabulary.txt

python bigram.py $@  | tr ' ' '_' | sort | uniq -c |tr '_' ' '| awk '{
		if ( $1 > 0 ) 
			 print $2 " " $3;
		}' > vocabulary.txt
