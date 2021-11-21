
run:
	docker-compose up -d --scale worker=3

build: build-dashboard build-producer build-worker build-queue

build-dashboard:
	cd dashboard && make build

build-producer:
	cd producer && make build

build-worker:
	cd worker && make build

build-queue:
	cd queue && make build