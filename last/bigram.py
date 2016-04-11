import sys

def gen_bigram (file):
	pf = open (file, 'r')
	words = pf.read().split()

	for i in xrange(len(words) - 1):
		print words[i], words[i + 1]
	pf.close()

gen_bigram (sys.argv[1])
gen_bigram (sys.argv[2])