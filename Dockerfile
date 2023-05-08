FROM python:3.9.16

RUN apt update && apt install tzdata -y && alias py=python
    # apt-get install cron -y

ENV TZ="Asia/Bangkok"
ENV PYTHONUNBUFFERED=TRUE

RUN pip install --upgrade pip

# WORKDIR /usr/src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]