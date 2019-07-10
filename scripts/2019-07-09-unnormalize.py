#! /usr/bin/env python3
#
# 2019-07-09 
# Colton Grainger 
# CC-0 Public Domain

"""
Unnormalize trees of metadata.
"""

import os
import sys
import errno
import magic
import csv

def pool_metadata(path, content_dict):
    """Collects metadata from csv text files at a given path,
    storing the key value pairs in the content dictionary.

    :path: Relative path to file.
    :content_dict: Dictionary to write out key-value pairs.
    :returns: Content dictionary, with metadata appended.

    """
    try:
        with open(path, newline='') as file:
            try:
                dialect = csv.Sniffer().sniff(
                        file.read(1024), delimiters=',\t')
                seems_to_be_csv = True
            except:
                seems_to_be_csv = False
            if seems_to_be_csv == True:
                file.seek(0)
                reader = csv.reader(file, dialect)
                key_value_pairs = {
                        rows[0].strip():rows[1].strip() 
                        for rows in reader if any(rows)} 
                content_dict = {
                        **content_dict, 
                        **key_value_pairs}
    except csv.Error as e:
        sys.exit('csv file: {}, line {}: {}'.format(
            path, reader.line_num, e))
    return content_dict

def catalog_content_under(path):
    """Catalogs the files and directories below the provided relative path,
    given metadata included as csv files in the directory tree.

    :path: Relative path to directory to be cataloged. Should be a directory.
    :returns: Nested json describing files, directories, and metadata.

    """
    content_dict = {}

    try:
        content_dict['contains'] = [
            catalog_content_under(os.path.join(path, content))
            for content in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        content_dict['type'] = 'file'
        content_dict['path'] = path 
        content_dict['media_type'] = magic.from_file(path, mime=True)

    if os.path.isdir(path):
        for content in os.listdir(path):
            p = os.path.join(path, content)
            if os.path.isfile(p):
                if "text" in magic.from_file(p, mime=True):
                    content_dict = pool_metadata(p, content_dict)
    
    return content_dict

import json
path = '/home/colton/fy/20/rda-image-archive/tests/template20190703_example_tree'
print(json.dumps(catalog_content_under(path), indent=2))
