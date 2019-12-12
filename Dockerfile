FROM python:3.7-slim

RUN apt-get update
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code

COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh

ENTRYPOINT ["init.sh"]