CONTAINER_RUNNER := $(if $(CONTAINER_RUNNER),$(CONTAINER_RUNNER),"docker")
CONTAINER_POSTGRES_IMAGE=bitnami/postgresql:16.4.0

################################################################################
# App
################################################################################
CONTAINER_POSTGRES_PORT=5432
POSTGRES_CONTAINER_NAME=ttrpg-pg
POSTGRES_DATABASE_NAME=ttrpg-pg

.PHONY: postgres-clean
postgres-clean: # removes local volume mount data
	@echo "removing postgres local volume mount defined in ~/projects/ttrpg/ttrpg-api/deploy/postgres/postgres.compose.yml"
	rm -rf ~/projects/ttrpg/volume-mounts/postgres

.PHONY: postgres-up
postgres-up:
	# start container if not already running
	${CONTAINER_RUNNER} start ${POSTGRES_CONTAINER_NAME} || ${CONTAINER_RUNNER} run --name ${POSTGRES_CONTAINER_NAME} -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRES_DB=${POSTGRES_DATABASE_NAME}\
		-e POSTGRESQL_PORT_NUMBER=${CONTAINER_POSTGRES_PORT}\
		-p ${CONTAINER_POSTGRES_PORT}:${CONTAINER_POSTGRES_PORT} ${CONTAINER_POSTGRES_IMAGE}

.PHONY: postgres-compose-up
postgres-compose-up:
	${CONTAINER_RUNNER} compose \
		-f ../deploy/postgres/postgres.compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		up -d

.PHONY: postgres-compose-down
postgres-compose-down:
	${CONTAINER_RUNNER} compose \
		-f ../deploy/postgres/postgres.compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		down

.PHONY: postgres-down
postgres-down:
	${CONTAINER_RUNNER} kill ${POSTGRES_CONTAINER_NAME}
	${CONTAINER_RUNNER} rm ${POSTGRES_CONTAINER_NAME}

.PHONY: postgres-kube-up
postgres-kube-up:
	echo "hello, workl"

################################################################################
# Testing
################################################################################
CONTAINER_POSTGRES_TEST_PORT=5433
POSTGRES_CONTAINER_NAME_TESTING=ttrpg-pg-testing
CONTAINER_POSTGRES_TEST_CONN=postgresql://postgres:admin@localhost:${CONTAINER_POSTGRES_TEST_PORT}/${POSTGRES_DATABASE_NAME}

.PHONY: postgres-up-testing
postgres-up-testing:
	# start container if not already running
	${CONTAINER_RUNNER} start ${POSTGRES_CONTAINER_NAME_TESTING} || ${CONTAINER_RUNNER} run --name ${POSTGRES_CONTAINER_NAME_TESTING} -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRES_DB=${POSTGRES_DATABASE_NAME}\
		-e POSTGRESQL_PORT_NUMBER=${CONTAINER_POSTGRES_TEST_PORT}\
		-p ${CONTAINER_POSTGRES_TEST_PORT}:${CONTAINER_POSTGRES_TEST_PORT} ${CONTAINER_POSTGRES_IMAGE}

.PHONY: postgres-down-testing
postgres-down-testing:
	${CONTAINER_RUNNER} kill ${POSTGRES_CONTAINER_NAME_TESTING}
	${CONTAINER_RUNNER} rm ${POSTGRES_CONTAINER_NAME_TESTING}
