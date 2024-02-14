#!/bin/bash

# Ask the user for the arguments
read -p "Enter db_file (default: db.json): " db_file
read -p "Enter taskid (default: 1): " taskid
read -p "Enter dir_path (default: taskid): " dir_path

# Use default values if the user didn't provide any
db_file=${db_file:-db.json}
taskid=${taskid:-1}
dir_path=${dir_path:-$taskid}

# Call the Python script with the provided arguments
python3 main.py -d $db_file -t $taskid -p $dir_path