#!/usr/bin/env python

# Collect a small sample of images from each of two years from the Todd folios
# For testing the image database

import sys
import os
import glob
from shutil import copy

# Disk with original images
image_source='/Volumes/Images/SA_Weather_folios'
# Selected subdirs
source_dirs = ('1883',
               '1933/1933 D (Met Data)')
# Take the first n
n_images = 12

for source_dir in source_dirs:
    images = sorted(glob.glob('%s/%s/*.jpg' % 
                              (image_source,source_dir)))[:n_images]

    target_dir = "%s/%s" % (os.path.dirname(__file__),
                            source_dir)

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    for image in images:
        copy(image,target_dir)



