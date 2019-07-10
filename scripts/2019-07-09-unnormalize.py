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

def flatten_catalog(catalog):
    flatdict = {k:v for k,v in catalog.items() if k != 'contains'}
    lowerdicts = catalog['contains']
    return tail_flatten_catalog(flatdict, lowerdicts)
    
def tail_flatten_catalog(flatdict,lowerdicts):

    behead = lambda catalog: {k:v for k,v in catalog.items() if k != 'contains'}

    assimilate = lambda flatdict, catalog: \
        tail_flatten_catalog(
                {**flatdict, **behead(catalog)}, catalog['contains']) \
        if 'contains' in set(catalog.keys()) \
        else {**flatdict, **catalog}

    return [assimilate(flatdict, catalog) for catalog in lowerdicts]

def tailflatten_list(flist,nlists):

    if nlists == []:
        return flist

    new_nlists = []
    new_flist = flist
    for nl in nlists:
        items = [i for i in nl if type(i) != list]
        lists = [l for l in nl if l not in items]
        new_flist.extend(items)
        new_nlists.extend(lists)
    return tailflatten_list(new_flist, new_nlists)

def flatten_list(nl):
  items = [i for i in nl if type(i) != list]
  lists = [l for l in nl if l not in items]
  return tailflatten_list(items, lists)

path = '/home/colton/fy/20/rda-image-archive/tests/template20190703_example_tree'

catalog = catalog_content_under(path)

flatten_list(flatten_catalog(catalog))
