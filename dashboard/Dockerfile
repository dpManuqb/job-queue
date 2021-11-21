FROM python:3.10.0-alpine

RUN apk update && apk upgrade
RUN apk add gcc musl-dev curl

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:9181/healthz || exit 1

CMD ["rq-dashboard"]