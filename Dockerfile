FROM python:3.7-alpine3.8

ADD . /app

WORKDIR /app

RUN apk add -U --no-cache -qq bash \
    && pip install --upgrade pip pipenv \
    && pip install -r requirements.txt

RUN pipenv install -dev

ENV MONGO_PASSWORD=L4yVXicZOGG1k73S

EXPOSE 5000

CMD python app.py