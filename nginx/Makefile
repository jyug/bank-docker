
DOCKER_IMAGE ?= nginx:latest
DOCKER_CONTAINER ?= proxy
SHELL := /bin/bash
VOLUME ?=-v $(PWD):/src -v $(DOCKER_CONTAINER)-venv:/venv
DOCKER_ENV ?=--rm -it
ENVIRONMENT ?= development
HIDE ?= @
PORT ?= 80
NETWORK := dev-network

network:
	-$(HIDE)docker network create --attachable -d bridge $(NETWORK) > /dev/null 2>&1 || true

.deps: # autogenerate .env for compose  with variables from Makefile
	$(HIDE)echo "$(foreach V,$(sort $(.VARIABLES)),$(if $(filter-out environment% default automatic,$(origin $V)),$V='$($V)'))"|xargs -n1 > .env
	$(HIDE)$(MAKE) network

pull:
	$(HIDE)docker pull nginx:latest

start: pull .deps
	$(HIDE)docker-compose -f docker/docker-compose.yml up $(DOCKER_CONTAINER)

stop: 
	$(HIDE)docker stop $(DOCKER_CONTAINER)
	$(HIDE)docker container rm $(DOCKER_CONTAINER)

daemon: pull .deps
	$(HIDE)docker-compose -f docker/docker-compose.yml up -d $(DOCKER_CONTAINER)