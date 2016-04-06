#!/bin/python

import sys
import math

with open(sys.argv[1], 'r') as myfile:
    pos=myfile.read().replace('\n', '')
   
with open(sys.argv[2], 'r') as myfile:
    neg=myfile.read().replace('\n', '')
      
with open(sys.argv[3],"r") as f:
    voc=f.readlines()
	
def train (pos, neg, voc):
   train_data = []
   for word in voc:
      train_data.append ([word, smooth(word, pos, len(voc)), smooth(word, neg, len(voc))])
 #    print "%s %f",word,smooth(word,pos,len(voc))
    
def count (word, text):
   return text.count (word)
   
def smooth(word, text, voc_size):
#   print count(word[:-1], text)
   return (math.log(count(word[:-1], text) + 1) - math.log (len(text.split()) + voc_size))

train(pos, neg, voc)
        
