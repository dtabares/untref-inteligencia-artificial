#!/usr/bin/python
import os
from PIL import Image

basewidth = 100

base_orig_path = '/home/dtabar/images/'
base_dest_path = '/home/dtabar/images/post_proc/'
r_types = ['glass','organic','paper','plastic']

def valid_image(file_name):
  return file_name.lower().endswith(('.png', '.jpg', '.jpeg'))


for r_type in r_types:
  path = base_orig_path + r_type + '/downloads'
  dest_path = base_dest_path + r_type
  dirs = os.listdir(path)
  for dir in dirs:
    image_dir = path + '/' + dir
    files = os.listdir(image_dir)
    for f in files:
      if valid_image(f):
        img_in = image_dir + '/' + f
        img_out = dest_path + '/' + f
        #print(img_in)
        #print(img_out)
        try:
          img = Image.open(img_in)
        except OSError:
          continue       
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img = img.convert('RGB')
        img.save(img_out)