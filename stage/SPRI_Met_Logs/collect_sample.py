#!/usr/bin/env python

# Collect a small sample of images from each of two SPRI logbooks
# For testing the image database

import sys
import os
import glob
from shutil import copy

# Disk with original images
image_source='/glade/scratch/brohan/Image_disc_copy/Nick_images/Scott Polar Research Institute'
# Selected subdirs
source_dirs = ('MS_74_SL','MS_548_8_2_SL')
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



