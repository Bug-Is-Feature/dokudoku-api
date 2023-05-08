#!/bin/bash

# echo -e "\nStart CRON service"
# service cron start

echo -e "\nApply database migrations"
python manage.py migrate

echo -e "\nLoad fixture data"
python manage.py loaddata achievement_groups
python manage.py loaddata achievements

echo -e "\nStarting server"
gunicorn -b 0.0.0.0:8000 --access-logfile '-' --error-logfile '-' --log-level info config.wsgi:application
