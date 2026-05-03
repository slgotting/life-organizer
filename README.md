
## 0. Create google oauth

- Go here: https://console.cloud.google.com/apis/credentials?project=organizer-bin-app
- Create new project
- Configure consent screen
- Create Client ID for web (at least) ; android may come later

## 1. Update configuration files in ./scripts/initialization/

```bash
vim scripts/initialization/find-and-replace.yml
```

## 2. Run scripts in ./scripts/initialization/

```bash
scripts/initialization/find-and-replace
```

## 3. Search for |UPDATE_ME| and update names by searching for each variable / string and doing replace all with vscode

## 4. Run the following:

```bash
cd frontend; npm i
npx cap add android; npx cap add ios
```

To see that nodemon vulnerability is not an issue since this is a devDependency run:

```bash
npm ls nodemon
```

## 5. Push to github and then set these secrets on github:

- DOCKER_USER
- DOCKER_PASSWORD
- SSH_KEY
- SSH_KEY_PASSPHRASE
- SUDO_PASSWORD
- ACCESS_TOKEN (gh-all.gpg)

## 5.5 If server needs the following, install them:
    - Docker
    - NGINX
    - Then run mongo docker container from home directory
        - docker run -p 27017:27017 --restart=unless-stopped -v ./mongo-data:/data/db -d mongo

## 5.75 Clone repo on the server into the following directories:
    - life-organizer
    - life-organizer-staging

## 5.875 USING PYTHON 3.10 (Because we know its compatible and we're focused on simplicity), create venv for each directory and pip install -r requirements.txt in them

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5.9 Create env file from .env.example and paste in real values
- frontend
- api

## 6. Set up DNS and NGINX by:

- Using domain host to point A records to:
    - @
    - staging
    - www
    - staging.api
    - api

- Follow the steps outlined [here](https://cheatsheets.slgotting.com/cheatsheets/linux/nginx#Set%20up%20TLS/SSL%20for%20HTTPS) to setup nginx (make sure to add all subdomains)
- Copy the contents of example_files/website.conf to your server /etc/nginx/conf.d/conffile.conf
- Run ```sudo nginx -t && sudo nginx -s reload```
- Copy contents of example_files/life_organizer.service and life_organizer-staging.service to /etc/systemd/system
- Run ```sudo systemctl daemon-reload & sudo sytemctl enable life_organizer.service & sudo systemctl start life_organizer.service & sudo sytemctl enable life_organizer-staging.service & sudo systemctl start life_organizer-staging.service ```

## 7. Set up maintenance cron jobs:
    - 5 5 * * * /home/steven/life-organizer/scripts/maintenance/backup_db.sh >> /var/log/slg/life-organizer/backup_db.log 2>&1

## 8. Make logo and update locations:

### Resize the background so that the logo takes up about half the total width and sits in the center of the transparent background
    - Do this by editing in gimp:
        - Image/Canvas Size
        - Increase by about 30-40%
        - Then use alignment tool, select your icon and center with buttons on left panel

#### Add logo into frontend/assets as logo-dark.png and logo.png
#### Then run, from ./frontend


npx @capacitor/assets generate --iconBackgroundColor '#eeeeee' --iconBackgroundColorDark '#111111' --splashBackgroundColor '#eeeeee' --splashBackgroundColorDark '#111111'

- frontend/static/favicon.png
- frontend/static/icon-only.png
## 9. Make sure release-checklist is done before releasing