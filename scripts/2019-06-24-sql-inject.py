#! /usr/bin/env python3
#
# 2019-06-24 
# Colton Grainger 
# CC-0 Public Domain

"""
Minimally inject images and metadata to SQL.
"""

import pandas as pd
import json
import os
from pathlib import Path
from pandas.io import sql
from sqlalchemy import create_engine
from pandas.io.json import json_normalize

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="steveaokiinthehouse858",
                               db="test"))

metadata_path = os.path.abspath(os.path.join(os.pardir, 'import', 'metadata'))

nara_jsons = [x for x in Path(metadata_path).glob('**/nara_id_*.json')]

nara_frames = []

for j in nara_jsons:
    with open(j) as f:
        nara_frames.append(json_normalize(
            json.load(f)['opaResponse']['results']['result'][0]))

for x in nara_frames[0]['objects.object'][0]:
    if not x['file']['@mime'] == 'application/pdf':
        print(x)
