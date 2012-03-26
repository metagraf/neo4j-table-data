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
		opts, args = getopt.getopt(sys.argv[1:], 'hi:o:v', ['help', 'input=','output='])
	except getopt.GetoptError, err:
		print str(err) # will print something like 'option -a not recognized'
		usage()
		sys.exit(2)
	verbose = False
	for o, a in opts:
		if o == '-v':
			verbose = True
		elif o in ('-h', '--help'):
			usage()
			sys.exit()
		elif o in ('-i', '--input'):
			input = a
		elif o in ('-o', '--output'):
			output = a
		else:
			assert False, 'unhandled option'

	if input == None or output == None: # requires input and output file
		print('Options -i and -o are both required, see help below.')
		usage()
		sys.exit()
	
	#create neo4j database
	db = create_database(output)
	
	#import data to neo4j database
	import_data(input, db)

	#shutdown database
	db.shutdown()

def create_database(database_name):	
	''' Create neo4j database '''
	db_obj = GraphDatabase(database_name)    
	return db_obj
	
def import_data(csv_file, database):
	''' Import data from CSV to neo4j database '''
	
	file_list = csv.reader(open(csv_file, 'rb'), delimiter=';', quotechar='|')
		
	# Create node index
	#  See http://docs.neo4j.org/chunked/snapshot/python-embedded-reference-indexes.html
	#  TODO Check if exists: exists = db.node.indexes.exists('my_nodes')
	with database.transaction:
		node_idx = database.node.indexes.create('my_nodes')
		
	node_attr_list = [] # create empty attribute list				
	i = 0
	for row in file_list: # loop each row in file
		if i == 0: # header row
		
			for col in row:
				node_attr_list.append(col) # save attribute names from first row
				
		else:
			with database.transaction:
				new_node = database.node()
				for col_num in range(len(node_attr_list)):
					new_node[node_attr_list[col_num]] = row[col_num]
					
				# Add the node to the index
				index_col_num = 0 # first column will be indexed
				node_idx[node_attr_list[index_col_num]][row[index_col_num]] = new_node
		i += 1
		
	print(str(i) + ' nodes were successfully added to the database.')

if __name__ == '__main__':
	''' Constructor; if = runs as script / else = runs as module '''	
	main(input, output)
else:
	pass


