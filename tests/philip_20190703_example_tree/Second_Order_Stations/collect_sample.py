#!/usr/bin/env python

# Collect a year's worth of images from the Second Order Stations book
# For testing the image database

import sys
import os
import glob
from shutil import copy

# Disk with original images
image_source='/Users/philip/Projects/SSO-Textract/images'
# Selected subdirs
source_dirs = ['1916']

for source_dir in source_dirs:
    images = sorted(glob.glob('%s/%s/page_????.jpg' % 
                              (image_source,source_dir)))

    target_dir = "%s/%s" % (os.path.dirname(__file__),
                            source_dir)

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    for image in images:
        copy(image,target_dir)



