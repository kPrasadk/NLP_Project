#! /usr/bin/python

ftr=open("neg.txt",'r')
new= open('datafile.txt','w')
stop=open('stopwords.txt','r')
stopwords= stop.read()
stopwords.split()
for line in ftr.readlines():
	line.lower()
	l=line.split()
	for word in l:
		if word not in stopwords:
			new.write(word)	
	new.write('/n')
print stopwords

