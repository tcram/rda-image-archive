#! /usr/bin/env python
#
# 2019-06-03 
# Colton Grainger 
# CC-0 Public Domain

"""
Script for unpacking/munging metadata in from a sample of ~2000 ship log images.
"""

import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
with open(os.path.join(parentDirectory, 'import','metadata/Idaho-BB-42-1944-05/nara_id_17298664.json' ) as f:
    data = json.load(f)

json_normalize(data['opaResponse']['results']['result'][0])
