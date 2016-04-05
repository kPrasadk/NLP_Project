#!/bin/python

import sys
import math
import pickle
import os
	
def train (pos, neg, voc):
   train_data = {}
   for word in voc:
		train_data[word] =  (smooth(word, pos, len(voc)), smooth(word, neg, len(voc)))
 #	print "%s %f",word,smooth(word,pos,len(voc))
	pickle.dump(train_data, "pickled.txt")
	
def count (word, text):
	return text.count (word)
   
def smooth(word, text, voc_size):
#   print count(word[:-1], text)
	return (math.log(count(word[:-1], text) + 1) - math.log (len(text.split()) + voc_size))

def get_train_data(pos_file, neg_file, iteration):
	top = iteration * 50 + 1;
	bottom = iteration * 50 + 50;
	os.system ("cat " + pos_file + " | head -" + bottom + " | tail -50 > test_pos.txt")
	os.system ("cat " + neg_file + " | head -" + bottom + " | tail -50 > test_neg.txt")
	os.system ("cat " + pos_file + " | head -" + (top - 1) + "> train_pos.txt")
	os.system ("cat " + pos_file + " | tail -" + (500 - bottom) + ">> train_pos.txt")
	os.system ("cat " + neg_file + " | head -" + (top - 1) + "> train_neg.txt")
	os.system ("cat " + neg_file + " | tail -" + (500 - bottom) + ">> train_neg.txt")
	os.system ("./createvoc.sh train_neg.txt train_pos.txt")

def test_review (train_data, review):
	pos_prob = 0.0
	neg_prob = 0.0
	for word in review.split():
		prob = train_data[word]
		pos_prob = pos_prob + prob[0]
		neg_prob = neg_prob + prob[1]
	
	return True if pos_prob > neg_prob else False
	
def test(pos, neg):
	with open (pos , 'r') as myfile:
		pos_lines = myfile.readlines ()
	with open (neg , 'r') as myfile:
		neg_lines = myfile.readlines ()
		
	train_data = pickle.load ("pickled.txt")
	correct = 0
	
	for review in pos_lines:
		if test_review (train_data, review):
			correct = correct + 1
	for review in neg_lines:
		if not test_review (train_data, review):
			correct = correct + 1
	print "Accuracy : " + correct + " of 100"
	
for i in xrange(10):
	get_train_data (sys.argv[1], sys.argv[2], i)
	with open("train_pos.txt", 'r') as myfile:
		pos = myfile.read().replace('\n', '')
   
	with open("train_neg.txt", 'r') as myfile:
		neg = myfile.read().replace('\n', '')
	  
	with open("vocabulary.txt","r") as f:
		voc = f.readlines()
	train (pos, neg, voc)
	test ("test_pos.txt", "test_neg.txt")
	
