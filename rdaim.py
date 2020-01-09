# TODO update metadata directory hierarchy for staging <ccg, 2019-06-26>

import pandas as pd
import json
import random
from pathlib import Path
import os

#  fakesection: set up logging for requests # 
import requests
import logging
import http.client

# https://stackoverflow.com/questions/16337511/
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

#  fakesection: import Wood's NARA metadata
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
df = pd.read_csv(os.path.join(parentDirectory, 'import', '2018-05-16-NARA-master-manifest/all.csv'))

# trim spaces and remove redundant column
df.rename(str.strip, axis='columns',inplace=True)
df.drop(columns=['Box or Volume Number.1'], inplace=True)

# Take sample from each record group;
# shuffling out N random ships to perform 
# a generalizable reaction from the frequencist's
# perspective. We parse and disbanden these. 
NARA_record_group_dict = dict([(23, 'USCS'), # Records of the Coast and Geodetic Survey
                               (24, 'Navy'), # Records of the Bureau of Naval Personnel
                               (26, 'CG'), # Records of the U.S. Coast Guard
                               (261, 'RAC') # Records of Former Russian Agencies
                              ])
sample = pd.concat([df.loc[df['Record Group'] == gp].sample(5, random_state=1)\
                    for gp in NARA_record_group_dict])

# drop entries without a valid NARA URL
ndf = sample[~sample['NARA URL'].str.contains(" ")]
# TODO pair all entries with valid NARA URLs <ccg, 2019-06-02>

#  fakesection: download each image under a given nara_id # 

def download_nara_entry(entry): # entry is assumed to be a *DataFrame*

    # access NARA API
    nara_id = entry['NARA URL'].iloc[0].split("/")[-1]
    api_base = 'https://catalog.archives.gov/api/v1/'
    api_url = '{0}?naIds={1}'.format(api_base, nara_id)
    res = requests.get(api_url)

    # metadata from Wood's all.csv (which is redundant, given NARA's metadata)
    # base_url = 'https://catalog.archives.gov/'
    # record_group = "rg-0{0}".format(int(entry['Record Group'].iloc[0]))
    # num_images = int(entry['Number of Images'].iloc[0])
    # digital_directory = ['Digital Directory'].iloc[0]

    # Parse NARA API output for metadata.
    entry_img_array = res.json() 
    object_img_array = entry_image_array[
            'opaResponse','results','result', 0, 'objects','object']
            # Only a *view* of the json, accessed by fancy indexing
            # an NumPy numerical array. <ccg, 2019-07-19>
        
    digital_directory = entry_img_array[0].get('file').get('@path').split("/")[-2]

    # create local directories if needed
    parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    paths = dict([(k,os.path.join(parentDirectory, 'import', k))\
                  for k in ['data', 'metadata']])
    for k, val in paths.items():
        p = Path(val)
        if (p.exists() == False and p.is_dir() == False):
            os.mkdir(val)

    # write NARA API output to file for reference
    api_output = "{0}/nara_id_{1}.json".format(paths['metadata'], digital_directory, nara_id)
    if res.status_code == 200:
        with open(api_output, 'wb') as f:
            f.write(res.content)

    # download all images for this unique nara_id
    for img_info in entry_img_array: 

        # test for mimetype "image/jpeg"
        # we don't want "application/pdf"
        if img_info.get('file').get('@mime') == "image/jpeg":

            img_name = img_info.get('file').get('@name')
            img_url = img_info.get('file').get('@url')
            img_res = requests.get(img_url)

            # create subdirectory if needed
            img_path = '{0}/nara_id_{1}'\
                       .format(paths['data'], digital_directory, nara_id)
            img_p = Path(img_path)
            if (img_p.exists() == False and img_p.is_dir() == False):
                os.mkdir(img_path)

            # write a single image to file
            local_img_name = "{0}/{1}".format(img_path, img_name)
            if img_res.status_code == 200:
                with open(local_img_name, 'wb') as img_f:
                    img_f.write(img_res.content)

return None

#  fakesection: actually download # 
ndf.groupby('NARA URL').apply(download_nara_entry)
#! /usr/bin/env python3
#
# 2019-06-10 
# Colton Grainger 
# CC-0 Public Domain

"""
Scrape json files for metadata to save as sql.
"""
# Woefully underprepared <ccg, 2019-07-10> # 

import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path
import os

metadata_path = os.path.abspath(os.path.join(os.pardir, 'import', 'metadata'))

nara_jsons = [x for x in Path(metadata_path).glob('**/nara_id_*.json')]
ia_jsons = [x for x in Path(metadata_path).glob('**/*.json') if not x.name.startswith('nara_id_')]

nara_frames = []
for j in nara_jsons:
    with open(j) as f:
        nara_frames.append(json_normalize(
            json.load(f)['opaResponse']['results']['result'][0]))

for x in nara_frames[0]['objects.object'][0]:
    if not x['file']['@mime'] == 'application/pdf':
        print(x)
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

def directory_crawl(dirpath):
    from pathlib import Path
    import os
    for filepath in sorted(Path(dirpath).glob('**/*')):
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

# TODO
# {sequential_uuid().hex : [str(image), magic.from_file(str(image), mime=True), os.path.getsize(str(image))] for image in find_images(os.path.join(git_repo_abs_dir(), "stage"))}
# DataFrame.from_dict(d, orient='index', columns=['file_path', 'mime_type', 'file_size'])
# df[df.mime_type.str.startswith("image")]
#! /usr/bin/env python3
#
# 2019-06-25 
# Colton Grainger 
# CC-0 Public Domain

"""
Attempts to flatten json structures and assign UUIDs from sample images.
"""

import subprocess
import configparser
import os
from sqlalchemy import create_engine

def git_repo_abs_dir():
    return subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel']).decode().rstrip()

def create_images_db_engine(defaults_extra_file):
    """Connects to the `images` database with sqlalchemy, given a 
    configuration file for the mysql client.

    :defaults_extra_file: A string that is the relative path to the
    configuration file specified by the --defaults-extra-file in the
    rda-image-archive repository's Makefile. Is relative to the root of the git
    repo.
    :returns: A sqlalchemy.engine.base.Engine object for use with pandas.

    """
    dbconfig = configparser.ConfigParser()
    dbconfig.read(os.path.join(git_repo_abs_dir(), defaults_extra_file))
    mysql_args = dict(dbconfig['client'])

    return create_engine("mysql+pymysql://{user}:{password}@{host}/images"
                           .format(**mysql_args))
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

def do_it(test_dir, csv_out):
	write_uuids_below(test_dir)
	df = frame_from_uuids_below(test_dir)
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
	df_images.to_csv(os.path.join(git_repo_abs_dir(), csv_out), 
			      index_label='image.image_id')
#! /usr/bin/env python3
#
# 2019-06-26 
# Colton Grainger 
# CC-0 Public Domain

"""
Convert directory metadata into nested json for ingest.
"""

# #  fakesection: to determine absolute paths
# import os
# import subprocess
# from pathlib import Path

# def git_repo_abs_dir():
#     return subprocess.check_output(
#             ['git', 'rev-parse', '--show-toplevel']).decode().rstrip()

# def found_files_below(some_path):
#     for filepath in sorted(Path(some_path).glob('**/*')):
#         if os.path.isfile(filepath):
#             yield filepath

# def staged_files_below(relative_path):
#     return found_files_below(os.path.join(git_repo_abs_dir(), relative_path))

# #  fakesection: to generate semi-sequential UUIDs 
# # answered 2019-05-16T13:46 by imposeren, CC-3.0 
# # https://stackoverflow.com/questions/56119272
# import time
# from random import getrandbits
# from uuid import uuid1, getnode

# fixed_seq = getrandbits(14)
# def sequential_uuid(node=None):
#     return uuid1(node=node, clock_seq=fixed_seq)
#     # .hex attribute of this value is a 32-character string
#     # these will give primary keys in type BINARY(16) for pages

# # fakesection: functionality for renaming to UUIDs (via a dictionary)
# import magic
# import json

# def uuids_below(relative_path):
#     """Makes UUID for all files at or below the given relative path in the repo.
#     :relative_path: Path relative to the root of the git repo.
#     :returns: Dictionary with UUIDs for keys and lists of absolute paths
#     media types, and file sizes as values.

#     """
#     return {sequential_uuid().hex :          # primary key
#         [
#          str(f),                             # absolute path
#          magic.from_file(str(f), mime=True), # mime type
#          os.path.getsize(str(f))             # size in bytes
#         ] 
#         for f in staged_files_below(relative_path)}

# def write_uuids_below(relative_path): 
#     """An imperative function that writes a dictionary of UUIDs naming all files
#     below a relative path.

#     :relative_path: Path relative to the root of the git repo.
#     :returns: None

#     """
#     uuid_dict = uuids_below(relative_path)
#     with open(os.path.join(git_repo_abs_dir(), 
#                            relative_path, 
#                            'uuid_dict.json'), 'w') as fp:
#         json.dump(uuid_dict, fp, indent=4)
#     pass
    
# def read_uuids_below(relative_path): 
#     """An imperative function that reads a dictionary of UUIDs

#     :relative_path: Path relative to the root of the git repo.
#     :returns: Dictionary

#     """
#     with open(os.path.join(git_repo_abs_dir(), 
#                            relative_path, 
#                            'uuid_dict.json'), 'r') as fp:
#         uuid_dict = json.load(fp)
#     return dict(uuid_dict)

# def rename_to_uuids_below(relative_path):
#     uuid_dict = read_uuids_below(relative_path)
#     for uuid in iter(uuid_dict):
#         os.rename(uuid_dict[uuid][0], os.path.join(git_repo_abs_dir(), relative_path, uuid))
#     pass

# def unname_from_uuids_below(relative_path):
#     uuid_dict = read_uuids_below(relative_path)
#     for uuid in iter(uuid_dict):
#         os.rename(os.path.join(git_repo_abs_dir(), relative_path, uuid), uuid_dict[uuid][0])
#     pass

# #  fakesection: importing and saving as a dataframe # 
# import pandas as pd
# from pandas import DataFrame, Series

# def frame_from_uuids_below(relative_path):
#     return DataFrame.from_dict(
#             read_uuids_below(relative_path), 
#             orient='index', 
#             columns=['absolute_path', 'mime_type', 'size_in_bytes']) 

# #  fakesection: imperatives # 

# write_uuids_below("stage")
# df = frame_from_uuids_below("stage")
# df_images = df[df.mime_type.str.startswith("image")]
# df_images = df_images.reindex(columns = df_images.columns.tolist() +
#                                         ['image.relative_order',
#                                         'document.relative_id_item',
#                                         'document.relative_id_value',
#                                         'document.start_date',
#                                         'document.end_date',
#                                         'platform.name',
#                                         'archive.name',
#                                         'archive.host_country'])
# df_images = df_images.rename({"absolute_path":"image.staging_path", 
#                               "mime_type":"image.media_subtype", 
#                               "size_in_bytes":"image.file_size"}, axis='columns')
# df_images.to_csv(os.path.join(git_repo_abs_dir(), "stage/flattened_metadata.csv"), 
#                       index_label='image.image_id')
import os
import errno
import magic
import csv

def path_hierarchy(path):
    hierarchy = {
        'type': 'directory',
        'name': os.path.basename(path),
        'path': path,
    }

    try:
        hierarchy['children'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        mime_type = magic.from_file(path, mime=True)
        hierarchy['type'] = mime_type
        if mime_type == "text/plain":
            try:
                with open(path, newline='') as csvfile:
                    dialect = csv.Sniffer().sniff(csvfile.read(1024))
                    csvfile.seek(0)
                    reader = csv.reader(csvfile, dialect)
                    metadata = {rows[0]:rows[1] for rows in reader if any(rows)} 
                    hierarchy['metadata'] = metadata
            except Exception as e:
                pass
        hierarchy['size'] = os.path.getsize(path)

    return hierarchy

if __name__ == '__main__':
    import json
    import sys

    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "."

    print(json.dumps(path_hierarchy(directory), indent=2, sort_keys=True))
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
        for content in os.listdir(path):
            p = os.path.join(path, content)
            _,ext = os.path.splitext(p)
            if os.path.isfile(p) and ext == '.csv':
                if "text" in magic.from_file(p, mime=True):
                    content_dict = pool_metadata(p, content_dict)
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        content_dict['type'] = 'file'
        content_dict['path'] = path 
        content_dict['media_type'] = magic.from_file(path, mime=True)
    return content_dict

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

def unnormalize_catalog(catalog):
    flatdict = {k:v for k,v in catalog.items() if k != 'contains'}
    lowerdicts = catalog['contains']
    return tail_unnormalize_catalog(flatdict, lowerdicts)

def flatten_list(nl):
      items = [i for i in nl if type(i) != list]
      lists = [l for l in nl if l not in items]
      return tail_flatten_list(items, lists)

def tail_unnormalize_catalog(flatdict,lowerdicts):
    behead = lambda catalog: {k:v for k,v in catalog.items() if k != 'contains'}
    assimilate = lambda flatdict, catalog: \
        tail_unnormalize_catalog(
                {**flatdict, **behead(catalog)}, catalog['contains']) \
        if 'contains' in set(catalog.keys()) \
        else {**flatdict, **catalog}
    return [assimilate(flatdict, catalog) for catalog in lowerdicts]

def tail_flatten_list(flist,nlists):
    if nlists == []:
        return flist
    new_nlists = []
    new_flist = flist
    for nl in nlists:
        items = [i for i in nl if type(i) != list]
        lists = [l for l in nl if l not in items]
        new_flist.extend(items)
        new_nlists.extend(lists)
    return tail_flatten_list(new_flist, new_nlists)

import json
def extract_and_unnormalize(path, **kwargs):
    catalog = catalog_content_under(path)
    metadata = flatten_list(unnormalize_catalog(catalog))
    output = kwargs.get('output', None)
    if output == 'write-json':
        with open(os.path.join(path, 'unnormalized_metadata.json'), 'w') as fp:
            json.dump(metadata, fp, indent=4)
    return metadata
    

if __name__ == '__main__':
# extract_and_unnormalize(os.getcwd(), output='write-json')
    import time
    t0=time.time()
    path = os.getcwd()
    metadata = catalog_content_under(path)
    with open(os.path.join(path, 'normalized_metadata.json'), 'w') as fp:
        json.dump(metadata, fp, indent=4)
    t1=time.time()
    with open(os.path.join(path, 'timed.json'), 'w') as tp:
        timed = t1 - t0
        info = {'timed':timed}
        json.dump(info, tp, indent=4)
#! /usr/bin/env python3
#
# 2019-07-11 
# Colton Grainger 
# CC-0 Public Domain

"""
Inject unnormalized json to MySQL database.
"""

import 
#! /usr/bin/env python3
#
# 2019-07-17
# Colton Grainger 

"""
Function definitions for the RDA images script (rdai).
"""

# from "__main__" section of rdai.py {{{ #

# import os.path, sys
# args = get_cli_arguments()

# # directory locations relative to RDAI installation
# rdai_dir = get_rdai_path()
# rdai_schema_dir = os.path.join(rdai_dir, "schema")
# rdai_script_dir = os.path.join(rdai_dir, "script")
# rdai_user_dir = os.path.join(rdai_dir, "user")

# # directory location for outputs
# output_dir = os.path.abspath(args.output_dir)
# debug("output directory: {}".format(output_dir))

# # directory location for data
# data_dir = os.path.abspath(args.data_dir)
# debug("data directory: {}".format(data_dir))

# config = get_config_info(rdai_script_dir, rdai_user_dir)
# plat = get_platform()
#  }}} fold # 

# args component definitions {{{ #

# if args.component == 'metadata':
#     if args.metadata_input in ['csv','json','xml']:
#         # TODO if catalog exists, raise warning and minimally update
#         # TODO unless forcing flag
#         create_catalog(data_dir, output_dir, args.metadata_input)
#     else:
#         raise NotImplementedError('cannot collect metadata from "{}" format'.format(args.metadata_input))

# elif args.component == 'uuid':
#     # TODO if uuid_dict exists, raise warning and minimally update
#     # TODO unless forcing flag
#     create_uuids(data_dir, output_dir)

# elif args.component == 'bundle':
#     # TODO test if uuid_dict and catalog exist
#     merge_uuids_into_catalog(output_dir)
#     # TODO optimize the tail-recursion
#     unnormalize_catalog(output_dir)
#     # TODO avoid frivilous updates with rsync (or shutils?)
#     rename_by_uuids(data_dir, output_dir)

# elif args.component == 'database':
#     # TODO test if bundle exists
#     # TODO unnormalized data as a DataFrame 
#     # TODO read MySQL config
#     # TODO inject (or update?) DataFrame

# else:
#     raise ValueError('the "{}" component is not a valid RDAI option'.format(args.component))
#  }}} #

# fakesection: messaging functions {{{ # 

# These functions were originally part of MathBook XML.
# Adapted from https://github.com/rbeezer/mathbook/tree/dev/script
# Copyright 2010-2016 Robert A. Beezer, released GPLv2

# 2016-05-05: this section should run under Python 2.7 and Python 3

# TODO why are these private functions?
# DONE date
def verbose(msg):
    """Write a message to the console on program progress"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 1:
            print('RDAI: {}'.format(msg))
    except NameError:
        print('RDAI: {}'.format(msg))

def debug(msg):
    """Write a message to the console with some raw information"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 2:
            print('RDAI-DEBUG: {}'.format(msg))
    except NameError:
        print('RDAI-DEBUG: {}'.format(msg))
#  }}} 

# fakesection: operating system functions {{{
# These functions were originally part of MathBook XML.
# Adapted from https://github.com/rbeezer/mathbook/tree/dev/script
# Copyright 2010-2016 Robert A. Beezer, released GPLv2

def get_rdai_path():
    """Returns path of root of RDAI distribution"""
    import sys, os.path
    verbose("discovering RDAI root directory from mbx script location")
    # full path to script itself
    rdai_path = os.path.abspath(sys.argv[0])
    # split "RDAI" executable off path
    script_dir, _ = os.path.split(rdai_path)
    # split "script" path off executable
    distribution_dir, _ = os.path.split(script_dir)
    verbose("RDAI distribution root directory: {}".format(distribution_dir))
    return distribution_dir


def get_source_path(source_file):
    """Returns path to content to be acted upon"""
    import sys, os.path
    verbose("discovering source directory from source location")
    # split path off filename
    source_dir, _ = os.path.split(source_file)
    return os.path.normpath(source_dir)

def get_executable(config, exec_name):
    "Queries configuration file for executable name, verifies existence in Unix"
    import os
    import platform
    import subprocess

    # http://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
    # suggests  where.exe  as Windows equivalent (post Windows Server 2003)
    # which  = 'where.exe' if platform.system() == 'Windows' else 'which'

    # get the name, but then see if it really, really works
    debug('locating "{}" in [executables] section of configuration file'.format(exec_name))
    config_name = config.get('executables', exec_name)

    devnull = open(os.devnull, 'w')
    try:
        result_code = subprocess.call(['which', config_name], stdout=devnull, stderr=subprocess.STDOUT)
    except OSError:
        print('RDAI:WARNING: executable existence-checking was not performed (e.g. on Windows)')
        result_code = 0  # perhaps a lie on Windows
    if result_code != 0:
        error_message = '\n'.join([
                        'cannot locate executable with configuration name "{}" as command "{}"',
                        'Edit the configuration file and/or install the necessary program'])
        raise OSError(error_message.format(exec_name, config_name))
    debug("{} executable: {}".format(exec_name, config_name))
    return config_name

def get_cli_arguments():
    """Return the CLI arguments in parser object"""
    import argparse
    parser = argparse.ArgumentParser(description='RDAI utility script', formatter_class=argparse.RawTextHelpFormatter)

    verbose_help = '\n'.join(["verbosity of information on progress of the program",
                              "  -v  is actions being performed",
                              "  -vv is some additional raw debugging information"])
    parser.add_argument('-v', '--verbose', help=verbose_help, action="count")

    component_info = [
        ('metadata', 'Metadata for data files.'),
        ('uuid', 'UUIDs for data files.'),
        ('bundle', 'Bundle from metadata, UUIDs, and data files.'),
        ('database', 'Database from bundle.'),
    ]
    component_help = 'Possible components are:\n' + '\n'.join(['  {} - {}'.format(info[0], info[1]) for info in component_info])
    parser.add_argument('-c', '--component', help=component_help, action="store", dest="component")

    metadata_input_info = [
        ('csv', 'Recursively read *.csv files in data directory. Format: "key","value".'),
        ('json', 'Recursively read *.json files in data directory. Format: {"key":"value"}.'),
        ('xml', 'Read single *.xml file from root of data directory. See docs for XML Schema.'),
    ]
    metadata_input_help = 'Possible metadata input formats are:\n' + '\n'.join(['  {} - {}'.format(info[0], info[1]) for info in metadata_input_info])
    parser.add_argument('-m', '--metadata-input', help=metadata_input_help, action="store", dest='metadata_input')

    parser.add_argument('-d', '--data-dir', help='path to data directory', action="store", dest='data_dir')
    parser.add_argument('-o', '--output-dir', help='path to output directory', action="store", dest='output_dir')
    return parser.parse_args()

    # "nargs" allows multiple options following the flag
    # separate by spaces, can't use "-stringparam"
    # stringparams is a list of strings on return
    # parser.add_argument('-p', '--parameters', nargs='+', help='stringparam options to pass to XSLT extraction stylesheet (option/value pairs)',
    #                      action="store", dest='stringparams')
    # # default to an empty string, which signals root to XSL stylesheet
    # parser.add_argument('-r', '--restrict', help='restrict to subtree rooted at element with specified xml:id',
    #                      action="store", dest='xmlid', default='')
    # parser.add_argument('-s', '--server', help='base URL for server (webwork only)', action="store", dest='server')

def sanitize_directory(dir):
    """Verify directory name, or raise error"""
    # Use with os.path.join, and do not sweat separator
    import os.path
    verbose('verifying directory: {}'.format(dir))
    if not(os.path.isdir(dir)):
        raise ValueError('directory {} does not exist'.format(dir))
    return dir

# Certificate checking is buggy, exception raised is malformed
# 2015/10/07 Turned off verification in three places
# Command line warning can be disabled, requests.packages.urllib3.disable_warnings()
def sanitize_url(url):
    """Verify a server address, append a slash"""
    verbose('validating, cleaning server URL: {}'.format(url))
    import requests
    try:
        requests.get(url, verify=False)
    except requests.exceptions.RequestException as e:
        root_cause = str(e)
        msg = "There was a problem with the server URL, {}\n".format(url)
        raise ValueError(msg + root_cause)
    # We expect relative paths to locations on the server
    # So we add a slash if there is not one already
    if url[-1] != "/":
        url = url + "/"
    return url

def sanitize_alpha_num_underscore(param):
    """Verify parameter is a string containing only alphanumeric and undescores"""
    import string
    allowed = set(string.ascii_letters + string.digits + '_')
    verbose('verifying parameter: {}'.format(param))
    if not(set(param) <= allowed):
        raise ValueError('param {} contains characters other than a-zA-Z0-9_ '.format(param))
    return param

def get_config_info(script_dir, user_dir):
    """Return configuation in object for querying"""
    import sys,os.path
    config_filename = "rdai.cfg"
    default_config_file = os.path.join(script_dir, config_filename)
    user_config_file = os.path.join(user_dir, config_filename)
    config_file_list = [default_config_file, user_config_file]
    # ConfigParser was renamed to configparser in Python 3
    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser
    config = configparser.SafeConfigParser()
    verbose("parsing configuration files: {}".format(config_file_list))
    files_read = config.read(config_file_list)
    debug("configuration files used/read: {}".format(files_read))
    if not(user_config_file in files_read):
        msg = "using default configuration only, custom configuration file not used at {}"
        verbose(msg.format(user_config_file))
    return config

def copy_data_directory(source_file, data_dir, tmp_dir):
    """Stage directory from CLI argument into the working directory"""
    import os.path, shutil
    verbose("formulating data directory location")
    source_full_path, _ = os.path.split(os.path.abspath(source_file))
    data_full_path = sanitize_directory(os.path.join(source_full_path, data_dir))
    data_last_step = os.path.basename(os.path.normpath(data_full_path))
    destination_root = os.path.join(tmp_dir, data_last_step)
    debug("copying data directory {} to working location {}".format(data_full_path, destination_root))
    shutil.copytree(data_full_path, destination_root)

def get_platform():
    """Return a string that tells us whether we are on Windows."""
    import platform
    return platform.system()

def is_os_64bit():
    """Return true if we are running a 64-bit OS.
    http://stackoverflow.com/questions/2208828/detect-64-bit-os-windows-in-python"""
    import platform
    return platform.machine().endswith('64')

def break_windows_path(python_style_dir):
    """Replace python os.sep with msys-acceptable "/" """
    import re
    return re.sub(r"\\", "/", python_style_dir)

# }}}

# fakesection: metadata functions {{{
# e.g., $ rdai -c metadata -m csv -d ~/data -o ~/tmp

# TODO def create_catalog(data_dir, output_dir, args.metadata_input):

def get_normalized_catalog(data_dir):
    """Catalogs the files and directories below the data_dir (relative path),
    given '.csv' or '.tsv' metadata (TODO or '.json') in the directory tree.

    :pool_metadata: "metadata gathering" function defined below.

    :data_dir: Relative path to directory to be cataloged. Should be a directory.
    :returns: Nested json describing files, directories, and metadata.

    """
    from pathlib import Path
    import os
    import magic

    # Initialize dictionary.
    normalized_catalog = {} 
    # Suppose data_dir is a parent.
    parent = Path(data_dir)

    if parent.is_dir():
        # List relative paths to children.
        children = [os.path.join(parent, x) for x in os.listdir(parent)]
        # Recurse down by calling `get_normalized_catalog` for each child.
        normalized_catalog['contents'] = [get_normalized_catalog(child) for child in children]
        # WARNING. We reserve the key 'contents' for inclusion of lists of child
        # dictionaries. Whence, the key 'contents' should appear 0 or 1 times in
        # each child dictionary.

        # Determine if `child` is a metadata tag file, and if so, in which input format.
        for child in children:
            _, ext = os.path.splitext(child)
            # TODO Test for xml and json.
            if ext in ['.csv', '.tsv']:
                # Update `normalized_catalog` with metadata from child.
                normalized_catalog = pool_metadata(child, normalized_catalog)

    # If the parent is not a directory, write out file-level metadata.
    # This is the floor of the recursive function call.
    else:
        normalized_catalog['file_path'] = str(parent)
        normalized_catalog['media_type'] = magic.from_file(parent, mime=True)
        # Eventually I'd like to restructure the program to recurse on
        # filetypes, so as to avoid reading headers redunandtly. At that
        # point, python-magic might not need to test for the file media_type. 2019-07-27

    return normalized_catalog

def pool_metadata(tagfile, normalized_catalog):
    """Collects key-value pairs from a given metadata tag file (here '.csv' or '.tsv'),
    then updates a given normalized catalog. TODO Add args for json or xml.

    :tagfile: Relative path to metadata file.
    :normalized_catalog: Dictionary to write out key-value pairs.
    :returns: Updated content dictionary.

    """
    # Initial state.
    to_parse = False 

    # Test the well-formedness of key/value pairs in the tagfile.
    try:
        with open(tagfile, newline='') as file:

            # Read head of CSV file and determine dialect.
            try:
                dialect = csv.Sniffer().sniff(file.read(2048), delimiters=',\t')
                # If we can parse the header, then toggle to_parse and read the rest.
                to_parse = True
            except csv.Error as e:
                verbose('CSV Sniffer failed to parse file: {}, error: {}'.format(tagfile, e))

            if to_parse:
                file.seek(0)
                reader = csv.reader(file, dialect)
                # Read the tagfile (for the first two fields from each non-empty row).
                key_value_pairs = {
                        rows[0].strip():rows[1].strip()
                        for rows in reader if any(rows)}
                        # To concatenate all rows 2+, try. <ccg, 2019-07-27> 
                        # rows[0].strip():[x.strip for x in rows[1:]]
                # Add key_value_pairs to the current level of the
                # normalized_catalog dictionary.
                normalized_catalog = {
                        **normalized_catalog,
                        **key_value_pairs}

    # Message for key/value error.
    except csv.Error as e:
        verbose('Syntax error: key-value pair in file: {}, line {}: {}'.format(
            tagfile, reader.line_num, e))

    # Return normalized_catalog updated with key/value pairs from tagile.
    return normalized_catalog

# }}}

# fakesection: uuid functions {{{
# abstracted from 2019-06-15-assign-uuids.py
# e.g., $ rdai -c uuid -d ~/data -o ~/tmp

def get_fixed_seq():
    """Declares/updates global fixed_seq, which seeds mind_uuid()."""
    global fixed_seq
    from random import getrandbits
    fixed_seq = getrandbits(14)

def mint_uuid(node=None):
    """Returns a semi-sequential uuid. Requires global fixed_seq to have been
    defined as a seed."""
    import time
    from uuid import uuid1, getnode
    # answered 2019-05-16T13:46 by imposeren, CC-3.0
    # <https://stackoverflow.com/questions/56119272>

    # get_fixed_seq() should be called prior to mint_uuid().
    global fixed_seq

    # Returns a 32-character hexadecimal string, which can be
    # stored in MySQL as BINARY(16) for efficient indexing. C.f.,
    # <https://mysqlserverteam.com/storing-uuid-values-in-mysql-tables/>
    return uuid1(node=node, clock_seq=fixed_seq).hex

def assign_uuid(filepath, overwrite=False):
    """Reads EXIF:ImageUniqueID tag for valid uuid. If no uuid exists, write
    mind_uuid() to EXIF:ImageUniqueID tag."""
    import exiftool
    with exiftool.ExifTool() as et:
        # By default, if the `EXIF:ImageUniqueID` tag is empty, uuid is assigned
        # to None.
        uuid = et.get_tag('ImageUniqueID', filepath)

        # If a uuid exists and overwrite is False, do nothing.
        if uuid != None and not overwrite:
            verbose("Tag EXIF:ImageUniqueID={} already exists in file {}.".format(uuid, filepath))

        # Else, no uuid was read by exiftool, or overwrite has been set to True.
        else:
            uuid = mint_uuid()
            et.execute_json('-ImageUniqueID={}'.format(uuid).encode(), filepath.encode())
            verbose("Wrote tag EXIF:ImageUniqueID={} to file {}.".format(uuid, filepath))

    # Pass either the read uuid from exiftool or the assigned from mint_uuid().
    return uuid

def get_files_under(data_dir):
    """Returns an iterator of posix paths to each file under data_dir. Is not sorted.

    :dir_path: Relative path to supposed directory.
    """

    from pathlib import Path
    for p in sorted(Path(data_dir).glob('**/*')):
        if p.is_file():
            yield p

def generate_uuids_under(data_dir):
    # TODO configuration file for assignment rules?
    """Creates a dictionary whose keys are paths relative to `scripts`
    and whose values are tuples of semi-sequentially assigned UUIDs.

    :data_dir: Relative path to data (image) files.
    :returns: Dictionary of UUIDs (assigned calling sequential_uuid()) and file extensions?

    """
    assignments = []
    for page in get_files_under(dirpath):
        page_ext = os.path.splitext(page)[1]
        assignments.extend((page, (sequential_uuid(), page_ext)))
    return assignments


{sequential_uuid().hex : [str(image), magic.from_file(str(image), mime=True), os.path.getsize(str(image))] for image in find_images(os.path.join(git_repo_abs_dir(), "stage"))}
DataFrame.from_dict(d, orient='index', columns=['file_path', 'mime_type', 'file_size'])
df[df.mime_type.str.startswith("image")]

# }}}

# fakesection: bundle functions {{{
# e.g., $ rdai -c bundle -d ~/data -o ~/tmp

# to unnormalize the json catalog in the output_dir ~/tmp
# TODO optimize recursive step <ccg, 2019-07-17> # 
def unnormalize_catalog(output_dir):

# to bundle the existing uuid_dict and catalog
def merge_uuids_into_catalog(output_dir):

# to rsync cataloged files from ~/data to ~/tmp and rename by uuid
# TODO avoid frivilous updates with rsync (or shutils?)
# TODO add configuration for remote output_dir <ccg, 2019-07-17> # 
def rename_by_uuids(data_dir, output_dir):

# }}}

# fakesection: database functions {{{
# e.g., $ rdai -c database -o ~/tmp
# to retrieve the database config and handle errors
# to initialize a test database with the rdai schema
# to inject bundled metadata into the test database
2019-06-25-create-sql-engine.py

# }}}

# fakesection: NARA functions {{{ # 

2019-06-01-sample-downloads.py
#  1}}} # 
#! /usr/bin/env python3
#
# 2019-07-10 
# Colton Grainger 
# 
# Adapted from https://github.com/rbeezer/mathbook/tree/dev/script
# Copyright 2010-2016 Robert A. Beezer
# These functions were originally part of MathBook XML.
# MathBook XML is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 or version 3.

"""
rdai utility script
"""

# fakesection: imports and function definitions {{{ # 

from rdai import *

# we also include these (otherwise private) cli-message functions

def verbose(msg):
    """Write a message to the console on program progress"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 1:
            print('RDAI: {}'.format(msg))
    except NameError:
        print('RDAI: {}'.format(msg))

def debug(msg):
    """Write a message to the console with some raw information"""
    try:
        global args
        # None if not set at all
        if args.verbose and args.verbose >= 2:
            print('RDAI-DEBUG: {}'.format(msg))
    except NameError:
        print('RDAI-DEBUG: {}'.format(msg))

#  1}}} # 

# fakesection: main {{{

# Parse command line
# Deduce some paths
# Read configuration file
# Switch on command line

import os.path, sys

# grab command line arguments
args = get_cli_arguments()
debug("CLI args {}".format(vars(args)))

# Report Python version in debugging output
msg = "Python version: {}.{}"
debug(msg.format(sys.version_info[0], sys.version_info[1]))

# directory locations relative to RDAI installation
rdai_dir = get_rdai_path()
rdai_schema_dir = os.path.join(rdai_dir, "schema")
rdai_script_dir = os.path.join(rdai_dir, "script")
rdai_user_dir = os.path.join(rdai_dir, "user")
debug("schema, script, and user directories: {}".format([rdai_schema_dir, rdai_script_dir, rdai_user_dir]))

# directory location for outputs
output_dir = os.path.abspath(args.output_dir)
debug("output directory: {}".format(output_dir))

# directory location for data
data_dir = os.path.abspath(args.data_dir)
debug("data directory: {}".format(data_dir))

config = get_config_info(rdai_script_dir, rdai_user_dir)
plat = get_platform()

if args.component == 'metadata':
    if args.metadata_input in ['csv','json','xml']:
        # TODO if catalog exists, raise warning and minimally update
        # TODO unless forcing flag
        create_catalog(data_dir, output_dir, args.metadata_input)
    else:
        raise NotImplementedError('cannot collect metadata from "{}" format'.format(args.metadata_input))

elif args.component == 'uuid':
    # TODO if uuid_dict exists, raise warning and minimally update
    # TODO unless forcing flag
    create_uuids(data_dir, output_dir)

elif args.component == 'bundle':
    # TODO test if uuid_dict and catalog exist
    merge_uuids_into_catalog(output_dir)
    # TODO optimize the tail-recursion
    unnormalize_catalog(output_dir)
    # TODO avoid frivilous updates with rsync (or shutils?)
    rename_by_uuids(data_dir, output_dir)

elif args.component == 'database':
    # TODO test if bundle exists
    # TODO unnormalized data as a DataFrame 
    # TODO read MySQL config
    # TODO inject (or update?) DataFrame

else:
    raise ValueError('the "{}" component is not a valid RDAI option'.format(args.component))
# 1}}}
