#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Author(s): Thomas Reinholdsson <reinholdsson@gmail.com>
# Info: https://github.com/reinholdsson/neo4j-table-data
# Created: 2012-03-28
# Updated: 2012-03-28

# DEFAULT OPTIONS
options = {'input': 'example/trade.csv', 'output': 'example/test.db', 'index': 'my_index'}

# HELP TEXT
help = ''' (to be added) '''

from neo4j import GraphDatabase
import csv, getopt, sys


def main(options):
	''' Main program '''	

	try:
		# Add command line parameters if any
		options = parameters(options)
		
		# Create neo4j database
		db = create_database(options['output'])
		
		# Import relationships to neo4j database
		import_relationships(options['input'], db, options['index'])
			
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
		opts, args = getopt.getopt(sys.argv[1:], 'hi:o:x:v', ['help', 'input=','output=', 'index='])
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
		elif o in ('-x', '--index'):
			options['index'] = a
		else:
			assert False, 'unhandled option'

	if options['input'] == None or options['output'] == None or options['index'] == None: # requires input and output file
		print('Options -i, -o and -x are all required, see help below.')
		usage()
		sys.exit()
		
	return options

def create_database(database_name):	
	''' Create neo4j database '''
	
	# TODO: Add db.shutdown() on error (try, except, else)?
	
	# Create or open neo4j database
	db_obj = GraphDatabase(database_name)
	
	return db_obj
	
def import_relationships(csv_file, db, index):
	''' Import relationships from CSV to neo4j database '''
	
	file_list = csv.reader(open(csv_file, 'rb'), delimiter=';', quotechar='|')

	# We perform changes from within transactions - either write all or none
	with db.transaction:
		
		# Get index
		if db.node.indexes.exists(index):
			node_idx = db.node.indexes.get(index)
		else:
			db.shutdown()
			# An index is required
			print('Index is missing')
			usage()
			sys.exit(2)
		
		# Options
		id_col_num = 1
		rel_col_num = 2
		index_lookup_attr = 'ccode'
				
		# Loop each row to create the nodes
		for row_id, row in enumerate(file_list): 
			if row_id == 0: # header row
				rel_attr_list = [] # create empty attribute list
				for col in row:
					rel_attr_list.append(col) # save attribute names from first row		
			else:
				
				#Look for items with the id
				first_node_hits = node_idx[index_lookup_attr][row[id_col_num]]
				for first_node in first_node_hits:
					#print(first_node)
					print('trade_id: ' + row[0])
					print(first_node['name'])
					second_node_hits = node_idx[index_lookup_attr][row[rel_col_num]]
					for second_node in second_node_hits:
						print(' ->' + second_node['name'])
						first_node.relationships.create('trade_with', second_node, trade=row[3])
						
						#Below is necessary if trade is both ways
						#TODO: add option on whether the relation is both ways 
						#second_node.relationships.create('trade_with', first_node, trade=row[3])
						#doesnt work - why?
						
					second_node_hits.close()	
				first_node_hits.close()					

	print 'Finished!'
	
if __name__ == '__main__':	
	main(options)
