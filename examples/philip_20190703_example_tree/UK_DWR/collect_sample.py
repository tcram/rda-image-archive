#!/usr/bin/env python

# Collect a small sample of images from a UK DWR volume
# For testing the image database

import sys
import os
import glob
import subprocess

# Disk with original images
image_source='/glade/scratch/brohan/Image_disc_copy//Catherine_Ross_DWR/1903A/DWR_1903_10.pdf'
# Take the first n
n_images = 10

target_dir = "%s/%s" % (os.path.dirname(__file__),
                        '1903')

if not os.path.isdir(target_dir):
    os.makedirs(target_dir)

cmd = 'pdfseparate %s %s/page_%%03d.pdf' % (image_source,target_dir)
proc = subprocess.Popen(cmd,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
    
images = sorted(glob.glob("%s/page_*.pdf" % target_dir))
count = 0
for image in images:
    if count<n_images:
        cmd = "sips -s format jpeg %s --out %s" % (image,
                                              image.replace('pdf','jpg'))
        proc = subprocess.Popen(cmd,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
    os.remove(image)
    count += 1




