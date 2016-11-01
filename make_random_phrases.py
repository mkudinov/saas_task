from random import randint

def make_random_phrases(data_source, number):
	vocab = []
	for line in open(data_source, 'r'):
		vocab.append(unicode(line, 'utf-8').strip())
		
	with open('random_phrases', 'w') as outf:	
		for i in range(number):
			rn = randint(10):
				if rn < 5:
					length = 2
				elif rn < 7:
					length = 3
				elif rn < 8:
					length = 1
				else:
					length = 4
			ngram = []
			for j in range(length):
				rn = randint(len(vocab))
				ngram.append(vocab[rn])
			ngram = u'_' + u'_'.join(vocab) + u'_'
			outf.write((u'%s\n' % ngram).encode('utf-8'))
		
