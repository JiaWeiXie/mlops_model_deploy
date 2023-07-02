SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

COMMA := ,

PROJECT_NAME := 'model-deploy'
PYTHON_IMAGE_VERSION := $(shell cat .python-version)

CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD  | sed -e 's/_/-/g; s/\//-/g')
CURRENT_VERSION := $(shell git rev-parse --short HEAD)

install: poetry install
.PHONY: install

venv: poetry shell
.PHONY: venv

lint-fix: ## Fix lint
	isort .
	black .
.PHONY: lint-fix

ci: lint typecheck test  ## Run all checks (lint, typecheck, test)
.PHONY: ci

clean:  ## Clean cache files
	find . -name '__pycache__' -type d | xargs rm -rvf
	find . -name '.mypy_cache' -type d | xargs rm -rvf
	find . -name '.pytest_cache' -type d | xargs rm -rvf
.PHONY: clean

docker-build: Dockerfile  ## Build docker image
	DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build \
		-f $^ \
		--build-arg PYTHON_IMAGE_VERSION=$(PYTHON_IMAGE_VERSION) \
		--tag $(PROJECT_NAME):$(CURRENT_BRANCH) \
		--tag $(PROJECT_NAME):$(CURRENT_VERSION) .
.PHONY: docker-build

py-dind-build: docker/pydind.Dockerfile  ## Build docker image
	docker build \
		-f $^ \
		--tag py311dind:$(CURRENT_BRANCH) \
		--tag py311dind:latest .
.PHONY: py-dind-build

py-dind-tag:
	docker image tag \
		py311dind:latest \
		localhost:5000/py311dind:latest
.PHONY: py-dind-tag


py-dind-push:
	docker image push \
		localhost:5000/py311dind:latest
.PHONY: py-dind-push

.DEFAULT_GOAL := help
help: Makefile
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help
