#!/usr/bin/python
import os
import random

base_orig_path = '/home/dtabar/images/post_proc/'
base_dest_path = '/home/dtabar/development/untref/ia/tp3/'
r_types = ['glass','organic','paper','plastic']

for r_type in r_types:
  path = base_orig_path + r_type
  files = os.listdir(path)
  num_of_files = len(files)
  test_set_size = int(num_of_files * 0.2)
  training_set_size = num_of_files - test_set_size
  i = 0
  print("Type: ", r_type)
  print("Number of files: ", num_of_files)
  print("Training set size: ", training_set_size)
  print("Test set size: ", test_set_size)

  while i < test_set_size:
    file_name = random.choice(files)
    files.remove(file_name)
    old_location = path + '/' + file_name
    new_location = base_dest_path + 'test_set/' + r_type + '/' + file_name
    #print("old_location :", old_location)
    #print("new_location :", new_location)
    os.rename(old_location, new_location)
    i = i + 1
  
  for f in files:
    old_location = path + '/' + f
    new_location = base_dest_path + 'training_set/' + r_type + '/' + f
    #print("old_location :", old_location)
    #print("new_location :", new_location)
    os.rename(old_location, new_location)
  print("-----------------------------------")