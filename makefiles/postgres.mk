CONTAINER_RUNNER := $(if $(CONTAINER_RUNNER),$(CONTAINER_RUNNER),"docker")
CONTAINER_PG_IMAGE=bitnami/postgresql:15.6.0

################################################################################
# App
################################################################################
CONTAINER_PG_PORT=5432
PG_DB_NAME=ttrpg-pg

.PHONY: postgres-up
postgres-up:
	# start container if not already running
	${CONTAINER_RUNNER} start ${PG_DB_NAME} || ${CONTAINER_RUNNER} run --name ${PG_DB_NAME} -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRESQL_PORT_NUMBER=${CONTAINER_PG_PORT}\
		-p ${CONTAINER_PG_PORT}:${CONTAINER_PG_PORT} ${CONTAINER_PG_IMAGE}

.PHONY: postgres-down
postgres-down:
	${CONTAINER_RUNNER} kill ${PG_DB_NAME}
	${CONTAINER_RUNNER} rm ${PG_DB_NAME}

################################################################################
# Testing
################################################################################
CONTAINER_PG_TEST_PORT=5433
CONTAINER_PG_TEST_CONN=postgresql://postgres:admin@localhost:${CONTAINER_PG_TEST_PORT}
PG_DB_TEST_NAME=ttrpg-pg-testing

.PHONY: postgres-up-testing
postgres-up-testing:
	# start container if not already running
	${CONTAINER_RUNNER} start ${PG_DB_TEST_NAME} || ${CONTAINER_RUNNER} run --name ${PG_DB_TEST_NAME} -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRESQL_PORT_NUMBER=${CONTAINER_PG_TEST_PORT}\
		-p ${CONTAINER_PG_TEST_PORT}:${CONTAINER_PG_TEST_PORT} ${CONTAINER_PG_IMAGE}

.PHONY: postgres-down-testing
postgres-down-testing:
	${CONTAINER_RUNNER} kill ${PG_DB_TEST_NAME}
	${CONTAINER_RUNNER} rm ${PG_DB_TEST_NAME}
