#!/bin/bash


# Create database and create db from mongo_latest.sif
# Create a new database test, and create a new user test with readWrite role
# creaete mongodb.log in $HOME/mongodb/log/ if not exist
mkdir -p $HOME/mongodb/log/
touch $HOME/mongodb/log/mongodb.log

export DB_PATH="/shared/Project/NCKU/Deep-SK/data/MongoDB"
export MONGODB_IMAGE=$HOME/mongo_latest.sif

singularity exec -B $DB_PATH/data/db:/data/db -B $HOME/log/:/var/log/ $MONGODB_IMAGE mongod --logpath /var/log/mongodb.log --dbpath /data/db 

# Wait for MongoDB to start
echo "Waiting for MongoDB to start"

# run mongosh and create a new database test, and create a new user test with readWrite role and password test
echo 'use test2
db.createUser(
  {
    user: "test",
    pwd: "test",
    roles: [ { role: "readWrite", db: "test" } ]
  }
)' | singularity exec mongo_latest.sif mongosh