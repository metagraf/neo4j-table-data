#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Author(s): Thomas Reinholdsson <reinholdsson@gmail.com>
# Info: https://github.com/reinholdsson/neo4j-table-data
# Created: 2012-03-24
# Updated: 2012-03-25

# TODO
# - add support for csv module
# - 
# -

from neo4j import GraphDatabase
import csv, getopt, sys

def main():
	''' The main method takes care of the option parameters, 
	for more information on how getopt works 
	please read http://www.doughellmann.com/PyMOTW/getopt/ '''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:v", ["help", "input=","output="])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-i", "--input"):
			input = a
		elif o in ("-o", "--output"):
			output = a
		else:
			assert False, "unhandled option"

	print("Input file: " + str(input))
	print("Output file: " + str(output))
	
if __name__ == "__main__":
	main()






