#!/usr/bin/python
import sys
import os

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

#pFile = open(qFile+"parsed")

