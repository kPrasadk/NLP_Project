#!/bin/python

import sys
import math
import pickle
import os
#import subprocess
import shlex
from subprocess import Popen, PIPE
from decimal import *

train_data = {}
mean_accuracy = 0
lambda1	= .9500000000000000000000000
lambda2 = .9500000000000000000000000

def train (pos, neg, voc_uni, voc_bi):
	print "Starting training."
	i = 0
	pos_count = len(pos.split())
	neg_count = len(neg.split())
	voc_size = len(voc_uni)
	total_len = len(voc_uni)+len(voc_bi) 
	for word in voc_uni:
		train_data[word] =  (smooth_uni(word, pos, pos_count, voc_size), smooth_uni(word, neg, neg_count, voc_size))
		#print train_data[word]
		i = i + 1
		print str(i * 100 / total_len) +"% " + word + " "*25 + "\r",	
	for word in voc_bi:
		train_data[word] =  (smooth_bi(word, pos, voc_size, 0), smooth_bi(word, neg, voc_size, 1))
		i = i + 1
		print str(i * 100 / total_len) +"% " + word + " "*25 + "\r",		
	print "Complete." + " " * 25
	#pickle.dump(train_data, "pickled.txt")
	
def count (word, text):
	return text.count (word)
   
def smooth_uni(word, text, num_words, voc_size):
	return  Decimal(lambda1) * Decimal(count(word, text))/ Decimal(num_words) + Decimal(1 - lambda1) * Decimal(1 / voc_size)
   
def smooth_bi(word, text, voc_size, index):
	f_word, s_word = word.split()
	prob = train_data.get(f_word)
	if prob is None:
		prob_uni = Decimal(1 - lambda1) * Decimal(1 / voc_size)
	else:
		prob_uni = prob[index]	
	return Decimal(lambda2) * Decimal(count(word, text)) / Decimal(count(f_word,text)+1) + Decimal(1 - lambda2) * Decimal(prob_uni) 

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

def test_review (train_data, review, pos, neg):
	pos_prob = Decimal(0.0)
	neg_prob = Decimal(0.0)
	rev_words = review.split()
	for word in [rev_words[i] + " " + rev_words[i + 1] for i in xrange(len(rev_words) - 1)]:
		prob = train_data.get(word)
		f_word, s_word = word.split()
		if prob is None:
			pos_prob += Decimal(0.0) #-math.log(count(f_word,pos) + len(voc))
			neg_prob += Decimal(0.0) #-math.log(count(f_word,neg) + len(voc))
		else :
			pos_prob = pos_prob + prob[0]
			neg_prob = neg_prob + prob[1]
	return True if pos_prob > neg_prob else False
	
def test(pos, neg, posstr, negstr):
	global mean_accuracy
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
		print str(progress * 100 / total_rev) + "%" + " "*25 + "\r", 
		if test_review (train_data, review, posstr, negstr):
			correct = correct + 1
	for review in neg_lines:
		progress = progress + 1
		print str(progress * 100 / total_rev) + "%" + " "*25 + "\r",
		if not test_review (train_data, review, posstr, negstr):
			correct = correct + 1
	mean_accuracy += correct
	print "Accuracy : " + str(correct) + " of 100"
	
os.system("setterm -cursor off")

for i in xrange(10):
	get_train_data (sys.argv[1], sys.argv[2], i)
	with open("train_pos.txt", 'r') as myfile:
		pos = myfile.read().replace('\n', ' ')
   
	with open("train_neg.txt", 'r') as myfile:
		neg = myfile.read().replace('\n', ' ')
	  
	with open("vocabulary_uni.txt","r") as f:
		voc_uni = f.read().split('\n')
	with open("vocabulary_bi.txt","r") as f:
		voc_bi = f.read().split('\n')	
	voc_uni = voc_uni[:-1]
	voc_bi = voc_bi[:-1]
	train_data={}
	train (pos, neg, voc_uni, voc_bi)
	test ("test_pos.txt", "test_neg.txt", pos, neg)

print "Mean accuracy: " + str(mean_accuracy / 10)
os.system("setterm -cursor on")

