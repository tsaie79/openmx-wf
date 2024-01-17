#!/bin/bash

export HOST_HOME="/home/jeng-yuantsai"

# Create database and create db ""
docker run -d -p 27017:27017 --name jiriaf_test_platform_db -v $HOST_HOME/JIRIAF/mongodb/data:/data/db mongo:latest

# Wait for MongoDB to start
echo "Waiting for MongoDB to start"
sleep 10

# Create a new user
echo "Creating a new user"
docker exec -it jiriaf_test_platform_db mongosh --eval 'db.getSiblingDB("ersap_hz_scale").createUser({user: "ersap", pwd: "ersap", roles: [{role: "readWrite", db: "ersap_hz_scale"}]})'