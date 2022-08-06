run: ## run the app
	LC_ALL=en_US.utf-8 LANG=en_US.utf-8 FLASK_ENV=development FLASK_APP=app flask run

test:  ## run tests locally
	pytest

test_ci:  ## run tests in a docker container. Meant for use on CI
	docker-compose run --rm app pytest

build_docker_local:  ## build docker image locally for testing
	docker build --build-arg SERVICE_NAME=PyBootcampCondaOmar-chaim . -t pybootcampcondaomar-chaim

refresh_requirements:  ## compile requirements from requirements.in to requirements.txt
	pip-compile -v --no-annotate requirements.in

help:	#### Support for help/self-documenting feature
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${MAKEFILE_LIST} | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: help

.DEFAULT_GOAL := help

