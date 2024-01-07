# INDIVIDUAL TO EACH DIRECOTRY
#    DOCKER_IMAGE
#    DOCKER_IMAGE_NAME
#    DOCKER_RUN_ARGS

GIT_TAG = $(shell git describe --tags --always --match="[0-9]*\.[0-9]*\.[0-9]*\-[a-z|0-9]*")
DOCKER_BUILD_FLAGES = TODO: build flags and use below
VERSION ?= ${GIT_TAG}
IMAGE_TAG ?= ${VERSION}



CONTAINER_REGISTRY = idkirk/ttrpg/builds
CONTAINER_RELEASE_REGISTRY = idkirk/ttrpg/releases

REGISTRY_IMAGE_TAG = $(CONTAINER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG)

CONTAINER_ID ?= $(shell docker ps | grep '$(REGISTRY_IMAGE_TAG)')

.PHONY: docker-clean
docker-clean: # build and tag container
	docker system prune --force
	docker volume prune --force

.PHONY: docker-build
docker-build: # build and tag container
	# TODO: $(DOCKER_BUILD_FLAGS)
	# docker build $(DOCKER_BUILD_FLAGS) -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG)
	docker build --network=host -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target development .

.PHONY: docker-build-production
docker-build-production: # build and tag container
  # TODO: $(DOCKER_BUILD_FLAGS)
	docker build --network=host -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target production .

.PHONY: docker-build-clean
docker-build-clean: # build and tag container
	# uses the --no-cache flag to rebuild from scratch
	docker build --no-cache --network=host -f image/Dockerfile -t $(REGISTRY_IMAGE_TAG) --target development .

.PHONY: docker-run
docker-run: # run container
	docker run -it $(DOCKER_RUN_ARGS) --name $(DOCKER_IMAGE_NAME) $(REGISTRY_IMAGE_TAG)
