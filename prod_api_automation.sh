# CURRENTLY UNUSED; NOT COMPLEX ENOUGH TO JUSTIFY USE
ROOT_PASSWORD=$1

PRODUCTION_DIR=/home/steven/life-organizer
PRODUCTION_API_DIR=/home/steven/life-organizer/api
PRODUCTION_FRONTEND_DIR=/home/steven/life-organizer/frontend

SERVICE_NAME=life_organizer.service


# install latest requirements (git fetch and reset mustve happened in github actions)
$PRODUCTION_API_DIR/venv/bin/pip3 install -r $PRODUCTION_API_DIR/requirements.txt

# build the cron jobs using tool; this is cool, consider using this in future
# $PRODUCTION_DIR/venv/bin/slg-build-cron-jobs -d $PRODUCTION_DIR/cron -u steven -v $PRODUCTION_DIR/venv/bin/python3

# stop the existing running server
echo $ROOT_PASSWORD | sudo -S systemctl stop $SERVICE_NAME

echo $ROOT_PASSWORD | sudo -S systemctl start $SERVICE_NAME