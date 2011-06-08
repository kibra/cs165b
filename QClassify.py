#!/usr/bin/python
import sys
import os
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets.classification import ClassificationDataSet, SequenceClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.connections import FullConnection
from pybrain.structure.modules import TanhLayer, LSTMLayer, LinearLayer, SigmoidLayer
from pybrain.structure import RecurrentNetwork

epochs = 10


POS = ["#","$","``","\'\'",",","-LRB-","-RRB-",".",":","?","CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNP","NNPS","NNS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"]
qClass = ["ABBREVIATION","abb","exp","ENTITY","animal","body","color","cremat","currency","dismed","event","food","instru","lang","letter","other","plant","product","religion","sport","substance","symbol","techmeth","termeq","veh","word","DESCRIPTION","definition","def","manner","reason","HUMAN","gr","ind","title","desc","LOCATION","city","country","mount","other","state","NUMERIC","code","count","date","dist","money","ord","other","period","perc","speed","temp","volsize","weight"]
def toBin(pos=None, q=None):
	if (q):
		return bin(qClass.index(q))[2:].rjust(6,"0")
	return bin(POS.index(pos))[2:].rjust(6,"0")

def toHash(word):
	result = 0
	for index, letter in enumerate(word):
		result += (index+1)*ord(letter)	
	return bin(result % 255)[2:].rjust(8,"0")

def trainSentence(sentence):
	#sentence is of the form: ['answer=X',(HASH,POS),...]
	for wordhash_wordtype in sentence[1:]:
		intuple = []
		outtuple = []
		for item in wordhash_wordtype[0]:
			intuple.append(int(item))
		for item in wordhash_wordtype[1]:
			intuple.append(int(item))
		for item in sentence[0]:
			if int(item) < 1:
				outtuple.append(-1)
			else:
				outtuple.append(int(item))
		print intuple, outtuple
		sds.appendLinked(intuple,outtuple)
		#print '('+wordhash_wordtype[0] + wordhash_wordtype[1]+'),('+sentence[0]+')'
	if len(sentence[1:]) > 0:
		print 'reset'
		sds.newSequence()

def testSentence(sentence):
	print "training----------"
	for wordhash_wordtype in sentence[1:]:
		intuple = []
		outtuple = []
		for item in wordhash_wordtype[0]:
			intuple.append(int(item))
		for item in wordhash_wordtype[1]:
			intuple.append(int(item))
		for item in sentence[0]:
			if int(item) < 1:
				outtuple.append(-1)
			else:
				outtuple.append(int(item))
		print intuple, outtuple
		result = rnet.activate(intuple)
	if (result != sentence[0])
		print "FAIL:",sentence
		exit(0)

#basically main
if __name__ == "__main__":
	#Initialize the ANN
	rnet = RecurrentNetwork()

	rnet.addInputModule(LinearLayer(8, name="word_hash"))
	rnet.addInputModule(LinearLayer(6, name="word_type"))
	rnet.addModule(LSTMLayer(6, name="hidden"))
	rnet.addOutputModule(TanhLayer(6, name="out"))

	rnet.addConnection(FullConnection(rnet["word_type"], rnet["hidden"]))
	rnet.addRecurrentConnection(FullConnection(rnet["hidden"], rnet["hidden"]))
	rnet.addConnection(FullConnection(rnet["hidden"], rnet["out"]))
	rnet.addConnection(FullConnection(rnet["word_hash"], rnet["out"]))

	rnet.sortModules()
	
	#Initialize the dataset
	sds = SequenceClassificationDataSet(14,6)
	
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
	
	for line in pFile:
		sentence = []
		for word in line.split(") (")[2:]:
			word = word.split(" ")
			if not(sentence):
				#print line
				sentence.append(toBin(q=word[1]))
			else:
				sentence.append((toHash(word[1]),toBin(word[0])))
		trainSentence(sentence)
	print "dataset created"
	
	trainer = BackpropTrainer(rnet, sds, learningrate=0.05)
	trainer.trainEpochs(epochs)
	
	#test
	if (argv[2]):
		#f = open(argv[2])
		exit(0)
	else
		#test with training data
		pFile = open(argv[1]+".parsed")
	
	for line in pFile:
		sentence = []
		for word in line.split(") (")[2:]:
			word = word.split(" ")
			if not(sentence):
				#print line
				sentence.append(toBin(q=word[1]))
			else:
				sentence.append((toHash(word[1]),toBin(word[0])))
		testSentence(sentence)
	
#	rnet.activate([0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1])
#	rnet.activate([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1])
#	rnet.activate([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0])
#	rnet.activate([1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0])
#	rnet.activate([0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0])
#	rnet.activate([0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1])
#	rnet.activate([0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1])
#	rnet.activate([0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0])
#	rnet.activate([1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1])
#	rnet.activate([0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1])
#	rnet.activate([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0])
#	rnet.activate([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0])
#	rnet.activate([0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0])
#	rnet.activate([0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0])
#	rnet.activate([0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1])
#	print rnet.activate([1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1])
#	rnet.reset()
#	print "Should out put: [1, -1, -1, -1, -1, 1]"
#	rnet.activate([0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1]) 
#	rnet.activate([0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1])
#	rnet.activate([0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0])
#	rnet.activate([0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1])
#	rnet.activate([0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0])
#	rnet.activate([1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0])
#	rnet.activate([1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0])
#	rnet.activate([0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0])
#	rnet.activate([1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1]) 
#	print rnet.activate([1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1])
#	rnet.reset()
#	print "Should out put: [-1, -1, 1, 1, 1, 1]"

