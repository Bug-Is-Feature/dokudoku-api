FROM python:3.9.16

RUN apt update && apt-get install cron -y && alias py=python

ENV PYTHONUNBUFFERED 1

# WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

# django-crontab logfile
# RUN mkdir /cron
# RUN touch /cron/django_cron.log

EXPOSE 8000

CMD service cron start && python manage.py crontab add && gunicorn config.wsgi:application