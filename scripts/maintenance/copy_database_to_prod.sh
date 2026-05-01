#!/bin/bash

read -p "Be careful with this script, it seems wrong"

read -p "Remember to update firewall! Press enter to begin"

# dump from local server; docker compose network must be running!
# mongodump --port 27017 --forceTableScan -d %%APP_ID%%-dev -c user -o /home/steven/dump

# # restore to staging
# mongosh %%APP_ID%%-staging --host %%SERVER_IP%% --eval "db.user.drop()"

# # restore to production
# mongosh %%APP_ID%%-prod --host %%SERVER_IP%% --eval "db.user.drop()"

# mongorestore --host %%SERVER_IP%% --port 27017 --nsInclude='%%APP_ID%%-dev.user' /home/steven/dump