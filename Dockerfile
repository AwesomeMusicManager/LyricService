FROM python:3.7-alpine3.8

WORKDIR /app

COPY . /app

RUN apk add -U --no-cache -qq bash \
    && pip install --upgrade pip pipenv \
    && pip install -r requirements.txt


EXPOSE 5000

RUN pipenv install -dev

CMD [ "python", "app.py" ]