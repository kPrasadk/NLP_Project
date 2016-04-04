#!/bin/bash

cat clean_pos.txt | tr ' ' '\n' | sort | uniq -c | awk '{
		if ( $1 > 1 ) 
			 print $2 ;
		}' > vocabulary.txt
