#FROM python:3.10.0

#RUN apt-get update && apt-get upgrade -y

FROM python:3.10.0-alpine

RUN apk update && apk upgrade
RUN apk add gcc musl-dev

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src src
WORKDIR /root/src

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD  rq info | grep -c $(ip -4 a | grep eth0 | tr " " "\n" | grep -A 1 inet | grep -E -o "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}") || exit 1

CMD ["rq", "worker", "--config", "settings"]