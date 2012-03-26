#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from neo4j import GraphDatabase

#open neo4j database
db = GraphDatabase('test.db')

#read
a_node = db.node[97]
print(a_node)

# Loop property values
for value in a_node.values():
    print(value)

#shutdown database
db.shutdown()
