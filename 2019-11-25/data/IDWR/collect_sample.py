#!/usr/bin/env python

# Collect a small sample of images from each of two IDWRs
# For testing the image database

import sys
import os
import glob
from shutil import copy

# Disk with original images
image_source='/glade/scratch/brohan/Image_disc_copy/Indian_Daily_Weather_Reports_NOAA'
# Selected subdirs
source_dirs = ('1892-07-01_1892-12-31',
               '1931-01-01_1931-06-30')
# Take the first n
n_images = 10

for source_dir in source_dirs:
    images = sorted(glob.glob('%s/%s/*.JPG' % 
                              (image_source,source_dir)))[:n_images]

    target_dir = "%s/%s" % (os.path.dirname(__file__),
                            source_dir)

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    for image in images:
        copy(image,target_dir)



