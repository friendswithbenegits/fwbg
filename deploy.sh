mv .env ..
git pull
sudo pip install -r requirements/production.txt
mv ../.env .
sudo supervisorctl restart all