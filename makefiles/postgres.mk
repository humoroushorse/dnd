DOCKER_PG_IMAGE=bitnami/postgresql:15.0.0

################################################################################
# App
################################################################################
DOCKER_PG_PORT=5432
PG_DB_NAME=dnd-pg

.PHONY: postgres-up
postgres-up:
	docker run --name ${PG_DB_NAME} -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRESQL_PORT_NUMBER=${DOCKER_PG_PORT}\
		-p ${DOCKER_PG_PORT}:${DOCKER_PG_PORT} ${DOCKER_PG_IMAGE}

.PHONY: postgres-down
postgres-down:
	docker kill ${PG_DB_NAME}
	docker rm ${PG_DB_NAME}

################################################################################
# Testing
################################################################################
DOCKER_PG_TEST_PORT=5433
DOCKER_PG_TEST_CONN=postgresql://postgres:admin@localhost:${DOCKER_PG_TEST_PORT}
PG_DB_TEST_NAME=dnd-pg-testing

.PHONY: postgres-up-testing
postgres-up-testing:
	docker run --name ${PG_DB_TEST_NAME} -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRESQL_PORT_NUMBER=${DOCKER_PG_TEST_PORT}\
		-p ${DOCKER_PG_TEST_PORT}:${DOCKER_PG_TEST_PORT} ${DOCKER_PG_IMAGE}

.PHONY: postgres-down-testing
postgres-down-testing:
	docker kill ${PG_DB_TEST_NAME}
	docker rm ${PG_DB_TEST_NAME}
