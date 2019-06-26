#!/usr/bin/env python

# Collect a small sample of images from each of two ADM53 logs
# For testing the image database

import sys
import os
import glob
from shutil import copy

# Disk with original images
image_source='/Volumes/Images/ADM_disc_7'
# Selected subdirs
source_dirs = ('ADM 53-68964','ADM 53-74447')
# Take the first n
n_images = 10

for source_dir in source_dirs:
    images = sorted(glob.glob('%s/%s/*.jpg' % 
                              (image_source,source_dir)))[:n_images]

    target_dir = "%s/%s" % (os.path.dirname(__file__),
                            source_dir)

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    for image in images:
        copy(image,target_dir)



