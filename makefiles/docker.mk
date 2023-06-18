# INDIVIDUAL TO EACH DIRECOTRY
#    DOCKER_IMAGE
#    DOCKER_RUN_ARGS

GIT_TAG = $(shell git describe --tags --always --match="[0-9]*\.[0-9]*\.[0-9]*\-[a-z|0-9]*")
DOCKER_BUILD_FLAGES = TODO: build flags and use below
VERSION ?= ${GIT_TAG}
IMAGE_TAG ?= ${VERSION}



CONTAINER_REGISTRY = idkirk/ttrpg/builds
CONTAINER_RELEASE_REGISTRY = idkirk/ttrpg/releases

REGISTRY_IMAGE_TAG = $(CONTAINER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG)


CONTAINER_ID ?= $(shell docker ps | grep '$(REGISTRY_IMAGE_TAG)')


.PHONY: docker-build
docker-build: # build and tag container
  # TODO: $(DOCKER_BUILD_FLAGS)
	# docker build $(DOCKER_BUILD_FLAGS) -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG)
	docker build --network=host -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target development .

.PHONY: docker-build-clean
docker-build-clean: # build and tag container
	# uses the --no-cache flag to rebuild from scratch
	docker build --no-cache --network=host -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target development .

.PHONY: docker-run
docker-run: # run container
	docker run -it --rm $(DOCKER_RUN_ARGS) $(REGISTRY_IMAGE_TAG)
