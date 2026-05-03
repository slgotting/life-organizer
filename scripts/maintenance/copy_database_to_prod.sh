#!/bin/bash

read -p "Be careful with this script, it seems wrong"

read -p "Remember to update firewall! Press enter to begin"

# dump from local server; docker compose network must be running!
# mongodump --port 27017 --forceTableScan -d life-organizer-dev -c user -o /home/steven/dump

# # restore to staging
# mongosh life-organizer-staging --host 127.0.0.1 --eval "db.user.drop()"

# # restore to production
# mongosh life-organizer-prod --host 127.0.0.1 --eval "db.user.drop()"

# mongorestore --host 127.0.0.1 --port 27017 --nsInclude='life-organizer-dev.user' /home/steven/dump