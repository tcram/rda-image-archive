#! /usr/bin/env python3
#
# 2019-06-15
# Colton Grainger 
# CC-0 Public Domain

"""
Assign UUIDs to all files (assumed to be pages) under the directory 
`import/data` in the rda-image-archive repo.
"""

#  fakesection: to generate semi-sequential UUIDs
import time
from random import getrandbits
from uuid import uuid1, getnode

# answered 2019-05-16T13:46 by imposeren, CC-3.0 
# https://stackoverflow.com/questions/56119272
fixed_seq = getrandbits(14)
def sequential_uuid(node=None):
    return uuid1(node=node, clock_seq=fixed_seq)
    # .hex attribute of this value is a 32-character string
    # these will give primary keys in type BINARY(16) for pages
    # https://mysqlserverteam.com/storing-uuid-values-in-mysql-tables/

#  fakesection: define the renaming as a dictionary mapping
from pathlib import Path
import os

path_to_pages = os.path.join(os.pardir, 'import', 'data')
path_for_export = os.path.join(os.pardir, 'export')

def find_pages(some_path):
    for filepath in sorted(Path(some_path).glob('**/*')):
        if os.path.isfile(filepath):
            yield filepath

def assign_uuids(iterator):
    """creates a dictionary whose keys are paths relative to `scripts`
    and whose values are tuples of semi-sequentially assigned UUIDs 
    and the original file extensions

    :iterator: iter object of posix_paths to pages (image files)
    :returns: dictionary of UUIDs (assigned calling sequential_uuid())
    and file extensions

    """
    assignments = []
    for page in iterator:
        page_ext = os.path.splitext(page)[1]
        assignments.extend((page, (sequential_uuid(), page_ext)))
    return assignments
