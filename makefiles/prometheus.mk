# prometheus.mk

# this file is imported
#    do not import other files
COMMON_REPOSITORY_ROOT=~/projects/ttrpg/ttrpg-api
CONTAINER_RUNNER := $(if $(CONTAINER_RUNNER),$(CONTAINER_RUNNER),"docker")
CONTAINER_PROJECT_NAME := $(if $(CONTAINER_PROJECT_NAME),$(CONTAINER_PROJECT_NAME),"ttrpg")


.PHONY: prometheus-compose-up
prometheus-compose-up:
	${CONTAINER_RUNNER} compose \
		-f ${COMMON_REPOSITORY_ROOT}/image/prometheus/docker-compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		up -d

.PHONY: prometheus-compose-down
prometheus-compose-down:
	${CONTAINER_RUNNER} compose \
		-f ${COMMON_REPOSITORY_ROOT}/image/prometheus/docker-compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		down
