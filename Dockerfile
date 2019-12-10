FROM python:3.7-slim

RUN apt-get update
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

ENV MONGO_PASSWORD=L4yVXicZOGG1k73S

COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh

EXPOSE 2222 5000

ENTRYPOINT ["init.sh"]
