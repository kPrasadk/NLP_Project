#!/usr/bin/python
import re
import sys

with open(sys.argv[1],"r") as f:
	content=f.readlines()

with open("stopwords.txt","r") as f:
	stopwords=f.readlines()

fw= open("clean_"+sys.argv[1],"w")

for j in range(len(stopwords)):
	stopwords[j]=stopwords[j].rstrip()	
	print stopwords[j]

for i in range(len(content)):
	content[i]=content[i].lower()
	content[i]=content[i].replace("&quot;","")
	content[i]=re.sub(r"[^a-z\ ]"," ",content[i])
	content[i]=" "+content[i]+" "
	for j in range(len(stopwords)):
		content[i]=content[i].replace(" "+stopwords[j]+" "," ")
	fw.write(content[i]+"\n")
	
print content[499]

