# make image
# make start

SHELL := /bin/bash
HIDE ?= @
DOCKER_IMAGE ?= team13/bank
DOCKER_CONTAINER ?= bank
VOLUME ?=-v $(PWD):/src -v $(DOCKER_CONTAINER)-venv:/venv
DOCKER_ENV ?=--rm -it
ENVIRONMENT ?= development
NETWORK := dev-network

.PHONY: image test lint docs

network:
	-$(HIDE)docker network create --attachable -d bridge $(NETWORK) > /dev/null 2>&1 || true

.deps: # autogenerate .env for compose  with variables from Makefile
	$(HIDE)echo "$(foreach V,$(sort $(.VARIABLES)),$(if $(filter-out environment% default automatic,$(origin $V)),$V='$($V)'))"|xargs -n1 > .env
	$(HIDE)$(MAKE) network

build:
	$(HIDE)docker build --build-arg GITHUB_TOKEN=$(GITHUB_TOKEN) -f Dockerfile -t $(DOCKER_IMAGE) $(PWD)
	$(HIDE)$(MAKE) install

install:
	$(HIDE)docker run -it --rm $(VOLUME) $(DOCKER_IMAGE) pip install -r requirements.txt --upgrade

start: .deps
	$(HIDE)docker-compose -f docker/docker-compose.yml up --no-recreate $(DOCKER_CONTAINER)

mysql: .deps
	$(HIDE)docker-compose -f docker/docker-compose.yml up -d --no-recreate mysql
	-$(HIDE)./docker/wait-for-it.sh mysql
	$(HIDE)docker exec mysql /docker-entrypoint-initdb.d/create-db.sh