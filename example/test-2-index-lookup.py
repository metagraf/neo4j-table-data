#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Test with index lookup

from neo4j import GraphDatabase

#open neo4j database
db = GraphDatabase('test.db')

#get index if it exists
if db.node.indexes.exists('my_nodes'):
	with db.transaction:
		node_idx = db.node.indexes.get('my_nodes')

#index lookup
hits = node_idx['abb']['SWD']
for a_node in hits:
	print(a_node)
	#loop property values
	for value in a_node.values():
		print(value)

#close index		
hits.close()

#shutdown database
db.shutdown()
