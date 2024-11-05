# CONTAINER_RUNNER=podman
CONTAINER_RUNNER := $(if $(CONTAINER_RUNNER),$(CONTAINER_RUNNER),"docker")
CONTAINER_PROJECT_NAME := $(if $(CONTAINER_PROJECT_NAME),$(CONTAINER_PROJECT_NAME),"ttrpg")
# INDIVIDUAL TO EACH DIRECOTRY
#    CONTAINER_IMAGE
#    CONTAINER_IMAGE_NAME
#    CONTAINER_RUN_ARGS

# GIT_TAG = $(shell git describe --tags --always --match="[0-9]*\.[0-9]*\.[0-9]*\-[a-z|0-9]*")
GIT_TAG = $(git describe --tags --always --match="[0-9]*\.[0-9]*\.[0-9]*\-[a-z|0-9]*")
# TODO: build flags and use below
CONTAINER_BUILD_FLAGES=""
VERSION_LATEST=latest
VERSION := $(if $(GIT_TAG),$(GIT_TAG),$(VERSION_LATEST))
IMAGE_TAG ?= ${VERSION}

CONTAINER_REGISTRY = idkirk/ttrpg/builds
CONTAINER_RELEASE_REGISTRY = idkirk/ttrpg/releases

REGISTRY_IMAGE_TAG = $(CONTAINER_REGISTRY)/$(CONTAINER_IMAGE):$(IMAGE_TAG)

CONTAINER_ID ?= $(shell ${CONTAINER_RUNNER} ps | grep '$(REGISTRY_IMAGE_TAG)')

.PHONY: container-clean
container-clean: # build and tag container
	${CONTAINER_RUNNER} kill $$(${CONTAINER_RUNNER} ps -a -q)
	${CONTAINER_RUNNER} system prune --volumes --force

.PHONY: container-build
container-build: # build and tag container
	# todo: build $(CONTAINER_BUILD_FLAGS)
	${CONTAINER_RUNNER} build --network=host -f deploy/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target development .

.PHONY: container-build-production
container-build-production: # build and tag container
  # TODO: $(CONTAINER_BUILD_FLAGS)
	${CONTAINER_RUNNER} build --network=host -f deploy/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target production .

.PHONY: container-build-clean
container-build-clean: # build and tag container
	# uses the --no-cache flag to rebuild from scratch
	${CONTAINER_RUNNER} build --no-cache --network=host -f deploy/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target development .

.PHONY: container-run
container-run: # run container
	${CONTAINER_RUNNER} run -it $(CONTAINER_RUN_ARGS) --name $(CONTAINER_IMAGE_NAME) $(REGISTRY_IMAGE_TAG)

.PHONY: contianer-rm
container-rm:
	# ${CONTAINER_RUNNER} kill ${CONTAINER_IMAGE_NAME}
	${CONTAINER_RUNNER} rm ${CONTAINER_IMAGE_NAME} --force
