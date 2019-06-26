#!/usr/bin/env python

# Collect a small sample of images from Weather Detective
# For testing the image database

import sys
import os
import glob
from shutil import copy

# Disk with original images
image_source='/Volumes/Images/Weather_Detective_images'
# Selected subdir
source_dir = 'January_1893'
# Take the first n
n_images = 10
images = sorted(glob.glob('%s/%s/*.JPG' % 
                          (image_source,source_dir)))[:n_images]

target_dir = "%s/%s" % (os.path.dirname(__file__),source_dir)

if not os.path.isdir(target_dir):
    os.makedirs(target_dir)
    
for image in images:
    copy(image,target_dir)



