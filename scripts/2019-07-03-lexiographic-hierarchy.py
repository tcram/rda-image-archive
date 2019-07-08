#! /usr/bin/env python3
#
# 2019-07-05 
# Colton Grainger 
# CC-0 Public Domain

"""
Requires input.csv file such that the first field 'id' contains strings that encode a lexiographic parent-child hiearchy.
Creates a json file describing such a hiearchy.
"""
# https://stackoverflow.com/questions/7408615 <ccg, 2019-07-05> # 
import csv
import json

class Node(dict):
    def __init__(self, start_node):
        dict.__init__(self)
        self['id'] = start_node[0]
        self['name'] = start_node[1].lstrip() # you have badly formed csv....
        self['description'] = start_node[2].lstrip()
        self['children'] = []

    def add_node(self, node):
        for child in self['children']:
            if child.is_parent(node):
                child.add_node(node)
                break
        else:
            self['children'].append(node)

    def is_parent(self, node):
        if len(self['id']) == 4 and self['id'][-1] == '0':
            return node['id'].startswith(self['id'][:-1])
        return node['id'].startswith(self['id'])

class RootNode(Node):
    def __init__(self):
        Node.__init__(self, ['Root', '', ''])

    def is_parent(self, node):
        return True

def pretty_print(node, i=0):
    print("{}ID={} NAME={} {}".format('\t' * i, node['id'], node['name'], node['description']))
    for child in node['children']:
        pretty_print(child, i + 1)

def main():
    with open('input.csv') as f:
        f.readline() # Skip first line
        root = RootNode()
        for node in map(Node, csv.reader(f)):
            root.add_node(node)

    pretty_print(root)
    print(json.dumps(root))

if __name__ == '__main__':
    main()

