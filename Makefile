
SHELL:=/bin/bash

WORKDIR_PATH=/simplepoll
REPO_PATH:=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
IMAGE_TAG?=pvphan/simplepoll:0.1
FLASK_PORT:=5000

RUN_FLAGS = \
	--rm \
	-it \
	--volume ${REPO_PATH}:${WORKDIR_PATH} \
	${IMAGE_TAG}

serve: image
	docker run \
		--publish ${FLASK_PORT}:${FLASK_PORT} \
		${RUN_FLAGS} \
		python3 app.py

shell: image
	docker run ${RUN_FLAGS} bash

image:
	docker build -t ${IMAGE_TAG} .

