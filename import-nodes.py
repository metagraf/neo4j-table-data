#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Author(s): Thomas Reinholdsson <reinholdsson@gmail.com>
# Info: https://github.com/reinholdsson/neo4j-table-data
# Created: 2012-03-25
# Updated: 2012-03-25

# OPTIONS (also ok to use command line arguments)
input = None  # structured data file to read
output = None # neo4j database folder

from neo4j import GraphDatabase
import csv, getopt, sys

def usage():
	''' Print help/information on how the program is to be used '''
	print('''
=========================================================================
Help/information
=========================================================================
	This is a script to import nodes from CSV to a neo4j database
	
	Example:
		python neo4j-table-data.py -i indata.csv -o mydatabase
		
	Options: 
		-i input, structured data file to read
		-o output, neo4j database folder
		-h help
		-v verbose
=========================================================================
	''')

def main(input, output):
	''' The main method takes care of the option parameters, 
	for more information on how getopt works 
	please read http://www.doughellmann.com/PyMOTW/getopt/ '''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:v", ["help", "input=","output="])
	except getopt.GetoptError, err:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
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

	if input == None or output == None: # requires input and output file
		print("Options -i and -o are both required, see help below.")
		usage()
		sys.exit()
	
	# If everything is OK then run program	
	run(input, output)
	
def run(input, output):
	''' Runs program '''
	print("Input: " + str(input))
	print("Output: " + str(output))
	
if __name__ == "__main__":
	''' Constructor; if = runs as script / else = runs as module '''	
	main(input, output)
else:
	pass


