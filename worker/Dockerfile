FROM python:3.10.0

RUN apt-get update && apt-get upgrade -y

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src src
WORKDIR /root/src

CMD ["rq", "worker", "--config", "settings"]