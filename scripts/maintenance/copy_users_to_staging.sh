#!/bin/bash

read -p "Remember to update firewall! Press enter to begin"

mongodump --port 27017 --forceTableScan -d life-organizer-dev -c user -o /home/steven/dump

mongorestore --host 127.0.0.1 --port 27017 --nsFrom='life-organizer-dev.user' --nsTo='life-organizer-staging.user' /home/steven/dump