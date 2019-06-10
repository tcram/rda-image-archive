#! /usr/bin/env python3
#
# 2019-06-10 
# Colton Grainger 
# CC-0 Public Domain

"""
Scrape json files for metadata to save as sql.
"""

import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path
import os

mpath = os.path.abspath(os.path.join(os.pardir, 'import', 'metadata'))

nara_jsons = [x for x in Path(mpath).glob('**/nara_id_*.json')]
ia_jsons = [x for x in Path(mpath).glob('**/*.json') if not x.name.startswith('nara_id_')]

nara_frames = []
for j in nara_jsons:
    with open(j) as f:
        nara_frames.append(json_normalize(
            json.load(f)['opaResponse']['results']['result'][0]))

for x in nara_frames[0]['objects.object'][0]:
    if not x['file']['@mime'] == 'application/pdf':
        print(x)
