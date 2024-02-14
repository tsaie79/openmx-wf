#!/bin/bash

cd /

echo "========================================"
echo "This script is to get preprocessed data of deepH from database."
echo "!!Warning:"
echo "Container must have the access to the host network to connect to the database. Default port is 27017."
echo "========================================"

export db_file=$1
export taskid=$2
export store_in=$3/deeph

# if $1 is empty, use default value "/deeph/db.json"
if [ -z "$db_file" ]; then
  export db_file="/deeph/db.json"
fi
mkdir -p $store_in
python3 /deeph/get_fs_data.py --db_file $db_file --taskid $taskid --store_in $store_in

