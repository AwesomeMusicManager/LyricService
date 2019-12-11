FROM python:3.7-slim

RUN apt-get update
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code

ENV PORT=5000

COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh

EXPOSE 5000

ENTRYPOINT ["init.sh"]