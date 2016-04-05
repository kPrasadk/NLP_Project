#!/bin/python

import sys
import math
import pickle
import os
#import subprocess
import shlex
from subprocess import Popen, PIPE

train_data = {}
	
def train (pos, neg, voc):
	print "Starting training."
	i = 0
	for word in voc:
		train_data[word] =  (smooth(word, pos, len(voc)), smooth(word, neg, len(voc)))
		i = i + 1
		print str(i * 100 / len(voc)) +"% " + word + " "*25 + "\r",	
	#pickle.dump(train_data, "pickled.txt")
	
def count (word, text):
	return text.count (word)
   
def smooth(word, text, voc_size):
	return (math.log(count(word, text) + 1) - math.log (len(text.split()) + voc_size))

def get_train_data(pos_file, neg_file, iteration):
	print "Fold Number "+str(iteration + 1)
	top = iteration * 50 + 1;
	bottom = iteration * 50 + 50;
	scriptfile = open ("temp_scr.sh", 'w')
	command = "head -" + str(bottom) + " " + pos_file + " | tail -50 > test_pos.txt" + "\n"
	command = command + "head -" + str(bottom) + " " + neg_file + " | tail -50 > test_neg.txt" + "\n" 
	command = command + "head -" + str(top - 1) + " " + pos_file + "> train_pos.txt" + "\n"
	command = command + "tail -" + str(500 - bottom) + " " + pos_file + ">> train_pos.txt" + "\n"
	command = command + "head -" + str(top - 1) + " " + neg_file + "> train_neg.txt" + "\n"
	command = command + "tail -" + str(500 - bottom) + " " + neg_file + ">> train_neg.txt" + "\n"
	command = command + "./createvoc.sh train_neg.txt train_pos.txt" + "\n"
	command = command + "echo 'Training and testing data created'" + "\n"
	scriptfile.write (command)
	scriptfile.close()	
	print "Generating training data."
	output = Popen(["bash", "temp_scr.sh", ], stdout=PIPE).communicate()[0]

def test_review (train_data, review, pos, neg, voc):
	pos_prob = 0.0
	neg_prob = 0.0
	for word in review.split():
		prob = train_data.get(word)
		
		if prob is None:
			pos_prob = 0 - ( math.log(len(pos.split()) + len(voc)))
			neg_prob = 0 - ( math.log(len(neg.split()) + len(voc)))
		else :
			pos_prob = pos_prob + prob[0]
			neg_prob = neg_prob + prob[1]
	return True if pos_prob > neg_prob else False
	
def test(pos, neg, posstr, negstr, vocstr):
	print "Testing phase."
	with open (pos , 'r') as myfile:
		pos_lines = myfile.readlines ()
	with open (neg , 'r') as myfile:
		neg_lines = myfile.readlines ()
		
	#train_data = pickle.load ("pickled.txt")
	correct = 0
	progress = 0
	total_rev = len(pos_lines) + len(neg_lines)
	
	for review in pos_lines:
		progress = progress + 1
		print str(progress * 100 / total_rev) + "%" + "\r", 
		if test_review (train_data, review, posstr, negstr, vocstr):
			correct = correct + 1
	for review in neg_lines:
		progress = progress + 1
		print str(progress * 100 / total_rev) + "%" + "\r",
		if not test_review (train_data, review, posstr, negstr, vocstr):
			correct = correct + 1
	
	print "Accuracy : " + str(correct) + " of 100"
	
os.system("setterm -cursor off")

for i in xrange(10):
	get_train_data (sys.argv[1], sys.argv[2], i)
	with open("train_pos.txt", 'r') as myfile:
		pos = myfile.read().replace('\n', ' ')
   
	with open("train_neg.txt", 'r') as myfile:
		neg = myfile.read().replace('\n', ' ')
	  
	with open("vocabulary.txt","r") as f:
		voc = f.read().split()
	train_data={}
	train (pos, neg, voc)
	test ("test_pos.txt", "test_neg.txt", pos, neg, voc)
	
