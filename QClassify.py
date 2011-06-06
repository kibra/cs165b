#!/usr/bin/python
import sys
import os

tokens = ["#","$","``","\'\'",",","-LRB-","-RRB-",".",":","CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNP","NNPS","NNS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"]
def toBin(pos):
	return bin(tokens.index(pos))[2:].rjust(6,"0")

def toHash(word):
	result = 0
	for index, letter in enumerate(word):
		result += (index+1)*ord(letter)
	return bin(result % 255)[2:].rjust(8,"0")

def trainsentence(sentence):
	#sentence is of the form: ['answer=X',(HASH,POS),...]
	print sentence

#basically main
if __name__ == "__main__":
	#The name of the file that contains the questions to classify.
	try:
		qFile = sys.argv[1]
		if not(os.path.isfile(qFile)):
			raise
	except:
		print "Usage: "+sys.argv[0]+" [FILE]"
		exit(1)
	#uses the Java library to add parts of speech
	os.system("java -classpath ./LBJPOS.jar edu.illinois.cs.cogcomp.lbj.pos.POSTagPlain ./"+qFile+" > "+qFile+".parsed")
	
	pFile = open(qFile+".parsed")
	
	#prove the token list
	#for index, item in enumerate(tokens):
	#	print str(index)+". \""+item
	for line in pFile:
		sentence = []
		for word in line.split(") (")[2:]:
			word = word.split(" ")
			if not(sentence):
				sentence.append("anwser="+word[1])
			else:
				sentence.append((toHash(word[1]),toBin(word[0])))
		trainsentence(sentence)
	
