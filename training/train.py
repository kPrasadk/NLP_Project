import sys

def train (pos, neg, voc):
   train_data = []
   for word in voc:
      train_data.append ((word, smooth(word, pos, len(voc)), smooth(word, neg, len(voc)))

def smooth(word, text, voc_size):
   return (count(word, text) + 1) / (len(text.split()) + voc_size)
   
def count (word, text):
   return text.count (word)
