#!/bin/bash
test_set_dir="/home/dtabar/development/untref/ia/tp3/test_set"
training_set_dir="/home/dtabar/development/untref/ia/tp3/training_set"
post_proc_dir="/home/dtabar/images/post_proc"
for d in `ls $test_set_dir`; do
  dir="$test_set_dir/$d/*"
  echo "executing command : rm $dir"
  rm $dir
done 

for d in `ls $training_set_dir`; do
  dir="$training_set_dir/$d/*"
  echo "executing command : rm $dir"
  rm $dir
done


for d in `ls $post_proc_dir`; do
  dir="$post_proc_dir/$d/*"
  echo "executing command : rm -rf $dir"
  rm $dir
done

echo "Running image pre proc python script"
python image-pre-proc.py

echo "Generating data sets"
python generate_sets.py