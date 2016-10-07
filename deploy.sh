mv .env ..
git pull
sudo pip install -r requirements/production.txt
mv ../.env .
python manage.py collectstatic --noinput
sudo supervisorctl restart all