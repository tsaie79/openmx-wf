#!/bin/bash

export HOST_HOME="/home/jeng-yuantsai"

# Create database and create db ""
docker run -d -p 27018:27017 --name hsin-openmx-wf -v $HOST_HOME/Hsin/mongodb/data:/data/db mongo:latest

# Wait for MongoDB to start
echo "Waiting for MongoDB to start"
sleep 10

# Create a new user
echo "Creating a new user"
docker exec -it hsin-openmx-wf mongosh --eval 'db.getSiblingDB("test").createUser({user: "test", pwd: "test", roles: [{role: "readWrite", db: "test"}]})'