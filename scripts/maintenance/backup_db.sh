#!/bin/bash

# Define MongoDB connection parameters
MONGO_HOST="localhost"
MONGO_PORT="27017"
MONGO_DB="%%APP_ID%%-prod"

HOME_DIR="/home/steven"

# Define backup directory
BACKUP_DIR="/home/steven/mongodb_backups"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Dump the MongoDB database to a timestamped backup file
TIMESTAMP=$(date "+%Y%m%d%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${MONGO_DB}_backup_$TIMESTAMP"
mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" --db "$MONGO_DB" --out "$BACKUP_FILE"

# Rotate backup files to keep only the last 5 dumps
cd $BACKUP_DIR; ls -1tr | head -n -5 | xargs -d '\n' rm -rf --

# Copy backup directory to other servers
REMOTE_SERVERS=("steven@159.89.80.11" "steven@104.131.67.101" "steven@138.197.73.21")

for server in "${REMOTE_SERVERS[@]}"; do
    ssh "$server" "rm -rf '$BACKUP_DIR'"
    scp -r "$BACKUP_DIR" "$server:/home/steven"
done
