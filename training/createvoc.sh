#!/bin/bash

cat $@ | tr ' ' '\n' | sort | uniq -c | awk '{
		if ( $1 > 1 ) 
			 print $2 ;
		}' > vocabulary.txt
