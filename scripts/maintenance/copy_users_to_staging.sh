#!/bin/bash

read -p "Remember to update firewall! Press enter to begin"

mongodump --port 27017 --forceTableScan -d %%APP_ID%%-dev -c user -o /home/steven/dump

mongorestore --host %%SERVER_IP%% --port 27017 --nsFrom='%%APP_ID%%-dev.user' --nsTo='%%APP_ID%%-staging.user' /home/steven/dump