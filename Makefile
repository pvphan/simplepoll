
SHELL:=/bin/bash

WORKDIR_PATH=/simplepoll
REPO_PATH:=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
IMAGE_TAG?=pvphan/simplepoll:0.1

RUN_FLAGS = \
	--rm \
	-it \
	--network=host \
	--volume=${REPO_PATH}:${WORKDIR_PATH} \
	${IMAGE_TAG}

shell: image
	docker run ${RUN_FLAGS} bash

image:
	docker build -t ${IMAGE_TAG} .

