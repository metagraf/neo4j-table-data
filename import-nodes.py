#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Author(s): Thomas Reinholdsson <reinholdsson@gmail.com>
# Info: https://github.com/reinholdsson/neo4j-table-data
# Created: 2012-03-25
# Updated: 2012-03-28

# DEFAULT OPTIONS
options = {'input': None, 'output': None}

# HELP TEXT
help = '''
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
'''

from neo4j import GraphDatabase
import csv, getopt, sys

def main(options):
	''' Main program '''	

	try:
		# Add command line parameters if any
		options = parameters(options)
		
		# Create neo4j database
		db = create_database(options['output'])
		
		# Import data to neo4j database
		import_data(options['input'], db)
			
		# Shutdown database
		db.shutdown()
	except getopt.GetoptError, err:
		print str(err)
		#pass # handle some exceptions
	else:
		return 0 # exit errorlessly

def usage():
	''' Print help/information on how the program is to be used '''

	print(help)

def parameters(options):
	''' Check if there are any optional command line parameters '''	

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
			options['input'] = a
		elif o in ('-o', '--output'):
			options['output'] = a
		else:
			assert False, 'unhandled option'

	if options['input'] == None or options['output'] == None: # requires input and output file
		print('Options -i and -o are both required, see help below.')
		usage()
		sys.exit()
		
	return options

def create_database(database_name):	
	''' Create neo4j database '''
	
	# TODO: Add db.shutdown() on error (try, except, else)?
	
	# Create or open neo4j database
	db_obj = GraphDatabase(database_name)
	
	return db_obj
	
def import_data(csv_file, db):
	''' Import data from CSV to neo4j database '''
	
	file_list = csv.reader(open(csv_file, 'rb'), delimiter=';', quotechar='|')
	
	# Count number of nodes (TODO: Option to deactive, might be slow with big data)
	#num_of_nodes_before = len(db.nodes)
	num_of_nodes = {'before': len(db.nodes)}
	
	# We perform changes from within transactions - either write all or none
	with db.transaction:
	
		# Create node index
		if db.node.indexes.exists('my_index'):
			node_idx = db.node.indexes.get('my_index')
		else:
			node_idx = db.node.indexes.create('my_index')

		# Loop each row to create the nodes
		for row_id, row in enumerate(file_list): 
			if row_id == 0: # header row
				node_attr_list = [] # create empty attribute list
				for col in row:
					node_attr_list.append(col) # save attribute names from first row		
			else:
					new_node = db.node()
					for col_num in range(len(node_attr_list)):
						new_node[node_attr_list[col_num]] = row[col_num]
					
					# Add the node to the index
					index_col_num = 0 # first column will be indexed (TODO: Add option)
					node_idx[node_attr_list[index_col_num]][row[index_col_num]] = new_node
	
	# Count number of successfully added nodes
	#num_of_nodes_after = len(db.nodes)
	num_of_nodes['after'] = len(db.nodes)
	num_of_nodes['added'] = num_of_nodes['after'] - num_of_nodes['before']	
	
	# Show results
	print "### Num of nodes ###\nBefore: %s\nAdded : %s\nAfter : %s"\
		% (num_of_nodes['before'], num_of_nodes['added'], num_of_nodes['after'])


if __name__ == '__main__':	
	main(options)



