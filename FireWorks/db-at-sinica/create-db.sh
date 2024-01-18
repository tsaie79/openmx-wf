#!/bin/bash

# Set the MongoDB image path
export MONGODB_IMAGE=$HOME/mongo_latest.sif

# Set the database name
export name_project="antisiteQubit"

# Create the users
singularity exec $MONGODB_IMAGE mongosh --eval "db.getSiblingDB('$name_project').createUser({user: 'Hsin', pwd: 'Hsin', roles: [{role: 'readWrite', db: '$name_project'}]});"
singularity exec $MONGODB_IMAGE mongosh --eval "db.getSiblingDB('$name_project').createUser({user: 'Hsin_ro', pwd: 'Hsin', roles: [{role: 'read', db: '$name_project'}]});"