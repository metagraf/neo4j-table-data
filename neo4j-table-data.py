#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Author(s): Thomas Reinholdsson <reinholdsson@gmail.com>
# Info: https://github.com/reinholdsson/neo4j-table-data
# Created: 2012-03-24
# Updated: 2012-03-25

# TODO
# - add support for csv module
# - warning before writing to a non-empty database
# - add the possibility to create relations and multiple nodes per line
# - allow specifying of which columns are the node identifiers, which coulums should be parameters on the nodes, which should be parameters on the relations and how to name and specify relations.
# - Perhaps convert to REST-bindings instead of embedded to be usable on e.g. Heroku? (I don't think they use embedded there, but not sure)

# OPTIONS - either one can set the options here or with the command line arguments
input = None  # structured data file to read
output = None # neo4j database folder

from neo4j import GraphDatabase
import csv, getopt, sys

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
		
def usage():
	''' Print help/information on how the program is to be used '''
	print('''
=========================================================================
Help/information
=========================================================================
	Example:
		python neo4j-table-data.py -i indata.csv -o mydatabase
		
	Options: 
		-i input, structured data file to read
		-o output, neo4j database folder
		-h help
		-v verbose
=========================================================================
	''')
	
def run(input, output):
	''' Runs program '''
	print("Input: " + str(input))
	print("Output: " + str(output))
	
if __name__ == "__main__":
	''' Constructor; if = runs as script / else = runs as module '''	
	main(input, output)
else:
	pass


