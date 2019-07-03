#! /usr/bin/env python3
#
# 2019-06-26 
# Colton Grainger 
# CC-0 Public Domain

"""
Exhibits an initial data exchange format (generated from NARA metadata).
"""

#  fakesection: to determine absolute paths
import os
import subprocess
from pathlib import Path

def git_repo_abs_dir():
    return subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel']).decode().rstrip()

def found_files_below(some_path):
    for filepath in sorted(Path(some_path).glob('**/*')):
        if os.path.isfile(filepath):
            yield filepath

def staged_files_below(relative_path):
    return found_files_below(os.path.join(git_repo_abs_dir(), relative_path))

#  fakesection: to generate semi-sequential UUIDs 
# answered 2019-05-16T13:46 by imposeren, CC-3.0 
# https://stackoverflow.com/questions/56119272
import time
from random import getrandbits
from uuid import uuid1, getnode

fixed_seq = getrandbits(14)
def sequential_uuid(node=None):
    return uuid1(node=node, clock_seq=fixed_seq)
    # .hex attribute of this value is a 32-character string
    # these will give primary keys in type BINARY(16) for pages

# fakesection: functionality for renaming to UUIDs (via a dictionary)
import magic
import json

def uuids_below(relative_path):
    """Makes UUID for all files at or below the given relative path in the repo.
    :relative_path: Path relative to the root of the git repo.
    :returns: Dictionary with UUIDs for keys and lists of absolute paths
    media types, and file sizes as values.

    """
    return {sequential_uuid().hex :          # primary key
        [
         str(f),                             # absolute path
         magic.from_file(str(f), mime=True), # mime type
         os.path.getsize(str(f))             # size in bytes
        ] 
        for f in staged_files_below(relative_path)}

def write_uuids_below(relative_path): 
    """An imperative function that writes a dictionary of UUIDs naming all files
    below a relative path.

    :relative_path: Path relative to the root of the git repo.
    :returns: None

    """
    uuid_dict = uuids_below(relative_path)
    with open(os.path.join(git_repo_abs_dir(), 
                           relative_path, 
                           'uuid_dict.json'), 'w') as fp:
        json.dump(uuid_dict, fp, indent=4)
    pass
    
def read_uuids_below(relative_path): 
    """An imperative function that reads a dictionary of UUIDs

    :relative_path: Path relative to the root of the git repo.
    :returns: Dictionary

    """
    with open(os.path.join(git_repo_abs_dir(), 
                           relative_path, 
                           'uuid_dict.json'), 'r') as fp:
        uuid_dict = json.load(fp)
    return dict(uuid_dict)

def rename_to_uuids_below(relative_path):
    uuid_dict = read_uuids_below(relative_path)
    for uuid in iter(uuid_dict):
        os.rename(uuid_dict[uuid][0], os.path.join(git_repo_abs_dir(), relative_path, uuid))
    pass

def unname_from_uuids_below(relative_path):
    uuid_dict = read_uuids_below(relative_path)
    for uuid in iter(uuid_dict):
        os.rename(os.path.join(git_repo_abs_dir(), relative_path, uuid), uuid_dict[uuid][0])
    pass

#  fakesection: importing and saving as a dataframe # 
import pandas as pd
from pandas import DataFrame, Series

def frame_from_uuids_below(relative_path):
    return DataFrame.from_dict(
            read_uuids_below(relative_path), 
            orient='index', 
            columns=['absolute_path', 'mime_type', 'size_in_bytes']) 

#  fakesection: imperatives # 

write_uuids_below("stage")
df = frame_from_uuids_below("stage")
df_images = df[df.mime_type.str.startswith("image")]
df_images = df_images.reindex(columns = df_images.columns.tolist() +
                                        ['image.relative_order',
                                        'document.relative_id_item',
                                        'document.relative_id_value',
                                        'document.start_date',
                                        'document.end_date',
                                        'platform.name',
                                        'archive.name',
                                        'archive.host_country'])
df_images = df_images.rename({"absolute_path":"image.staging_path", 
                              "mime_type":"image.media_subtype", 
                              "size_in_bytes":"image.file_size"}, axis='columns')
df_images.to_csv(os.path.join(git_repo_abs_dir(), "stage/flattened_metadata.csv"), 
                      index_label='image.image_id')
