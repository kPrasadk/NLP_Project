#!/bin/python

import sys
import math
import pickle
import os
import subprocess
import shlex

train_data = {}
	
def train (pos, neg, voc):
	train_data = {}
	for word in voc:
		train_data[word] =  (smooth(word, pos, len(voc)), smooth(word, neg, len(voc)))
	print train_data		
	#pickle.dump(train_data, "pickled.txt")
	
def count (word, text):
	return text.count (word)
   
def smooth(word, text, voc_size):
#   print count(word[:-1], text)
	return (math.log(count(word, text) + 1) - math.log (len(text.split()) + voc_size))

def get_train_data(pos_file, neg_file, iteration):
	print "Inside "+str(iteration)+" iteration"
	top = iteration * 50 + 1;
	bottom = iteration * 50 + 50;
	scriptfile = open ("temp_scr.sh", 'w')
	command = "cat " + pos_file + " | head -" + str(bottom) + " | tail -50 > test_pos.txt" + "\n"
	command = command + "cat " + neg_file + " | head -" + str(bottom) + " | tail -50 > test_neg.txt" + "\n" 
	command = command + "cat " + pos_file + " | head -" + str(top - 1) + "> train_pos.txt" + "\n"
	command = command + "cat " + pos_file + " | tail -" + str(500 - bottom) + ">> train_pos.txt" + "\n"
	command = command + "cat " + neg_file + " | head -" + str(top - 1) + "> train_neg.txt" + "\n"
	command = command + "cat " + neg_file + " | tail -" + str(500 - bottom) + ">> train_neg.txt" + "\n"
	command = command + "./createvoc.sh train_neg.txt train_pos.txt" + "\n"
	command = command + "echo 'Training and testing data created'" + "\n"
	scriptfile.write (command)
	scriptfile.close()	
	#os.system ("bash temp_scr.sh")
	subprocess.call(shlex.split ("bash temp_scr.sh"))

def test_review (train_data, review, pos, neg, voc):
	pos_prob = 0.0
	neg_prob = 0.0
	for word in review.split():
		prob = train_data.get(word)
		
		print prob
		if prob is None:
			pos_prob = 0 - ( math.log(len(pos.split()) + len(voc)))
			neg_prob = 0 - ( math.log(len(neg.split()) + len(voc)))
		else :
			pos_prob = pos_prob + prob[0]
			neg_prob = neg_prob + prob[1]
	print "Positive: " + str(pos_prob) + "Neg: " + str(neg_prob)
	return True if pos_prob > neg_prob else False
	
def test(pos, neg, posstr, negstr, vocstr):
	print "Testing................... "
	with open (pos , 'r') as myfile:
		pos_lines = myfile.readlines ()
	with open (neg , 'r') as myfile:
		neg_lines = myfile.readlines ()
		
	#train_data = pickle.load ("pickled.txt")
	correct = 0
	
	for review in pos_lines:
		if test_review (train_data, review, posstr, negstr, vocstr):
			correct = correct + 1
	for review in neg_lines:
		if not test_review (train_data, review, posstr, negstr, vocstr):
			correct = correct + 1
	
	print "Accuracy : " + str(correct) + " of 100"
	
for i in xrange(10):
	get_train_data (sys.argv[1], sys.argv[2], i)
	with open("train_pos.txt", 'r') as myfile:
		pos = myfile.read().replace('\n', ' ')
   
	with open("train_neg.txt", 'r') as myfile:
		neg = myfile.read().replace('\n', ' ')
	  
	with open("vocabulary.txt","r") as f:
		voc = f.read().split()
	train (pos, neg, voc)
	test ("test_pos.txt", "test_neg.txt", pos, neg, voc)
	
