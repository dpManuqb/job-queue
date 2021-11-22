FROM python:3.10.0-alpine

RUN apk update && apk upgrade
RUN apk add gcc musl-dev

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src src
WORKDIR /root/src  

CMD ["rq", "worker", "--config", "settings"]