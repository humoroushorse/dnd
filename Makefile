DOCKER_PG_IMAGE=bitnami/postgresql:15.0.0
DOCKER_PG_PORT=5432

################################################################################
# App
################################################################################
.PHONY: docker-pg-up
docker-pg-up:
	docker run --name dnd-pg -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRESQL_PORT_NUMBER=${DOCKER_PG_PORT}\
		-p ${DOCKER_PG_PORT}:${DOCKER_PG_PORT} ${DOCKER_PG_IMAGE}

.PHONY: pydnd-docker-pg-alembic-upgrade
pydnd-docker-pg-alembic-upgrade:
	# passing in override variable `db_override` to be read in `alembic/env.py`
	cd pydnd && poetry run alembic upgrade head

.PHONY: pydnd-docker-db-up
pydnd-docker-db-up:
	make docker-pg-up
	sleep 2
	make pydnd-docker-pg-alembic-upgrade
	make pydnd-load-seeds

.PHONY: pydnd-start
pydnd-start:
	cd pydnd && poetry env use python3 && poetry run uvicorn app.dnd.main:app

.PHONY: pydnd-mkdocs
pydnd-mkdocs:
	cd pydnd && poetry run mkdocs serve --dev-addr=0.0.0.0:8001

################################################################################
# Testing
################################################################################
DOCKER_PG_TEST_PORT=5433
DOCKER_PG_TEST_CONN=postgresql://postgres:admin@localhost:${DOCKER_PG_TEST_PORT}

PYDND_TEST_PATH=app/dnd/tests
PYDND_COVERAGE_PATH=htmlcov/pydnd
PYDND_INTEGRATION_TEST_PATH=${PYDND_TEST_PATH}/integration
PYDND_INTEGRATION_COVERAGE_PATH=${PYDND_COVERAGE_PATH}/integration
PYDND_UNIT_TEST_PATH=${PYDND_TEST_PATH}/unit
PYDND_UNIT_COVERAGE_PATH=${PYDND_COVERAGE_PATH}/unit

.PHONY: docker-pg-tests-up
docker-pg-tests-up:
	docker run --name dnd-pg-tests -d\
		-e POSTGRESQL_USERNAME=postgres\
		-e POSTGRESQL_PASSWORD=admin\
		-e POSTGRESQL_PORT_NUMBER=${DOCKER_PG_TEST_PORT}\
		-p ${DOCKER_PG_TEST_PORT}:${DOCKER_PG_TEST_PORT} ${DOCKER_PG_IMAGE}

# passing in override variable `db_override` to be read in `alembic/env.py`
.PHONY: pydnd-docker-pg-tests-alembic-upgrade
pydnd-docker-pg-tests-alembic-upgrade:
	cd pydnd && poetry run alembic -x db_override=${DOCKER_PG_TEST_CONN} upgrade head

.PHONY: docker-db-tests-up
docker-db-tests-up:
	make docker-pg-tests-up
	sleep 2
	make pydnd-docker-pg-tests-alembic-upgrade

.PHONY: pydnd-unit
pydnd-unit:
	cd pydnd && poetry run pytest ${PYDND_UNIT_TEST_PATH} -v --cov=app

.PHONY: pydnd-unit-html
pydnd-unit-html:
	cd pydnd && poetry run pytest ${PYDND_UNIT_TEST_PATH} -v --cov=app --cov-report=html:${PYDND_UNIT_COVERAGE_PATH} && open ${PYDND_UNIT_COVERAGE_PATH}/index.html

# For integration: create clean database and then run integration tests
.PHONY: pydnd-integration
pydnd-integration:
	make docker-db-tests-up
	# run the tests and even if they fail, destroy the docker container
	cd pydnd && poetry run pytest ${PYDND_INTEGRATION_TEST_PATH} --seed="${SEED}" --skip-d20="${SKIP_D20}" --maxfail=1 -v --cov=app || echo "continuing even if error"
	docker kill dnd-pg-tests
	docker rm dnd-pg-tests

.PHONY: pydnd-integration-html
pydnd-integration-html:
	cd pydnd && poetry run pytest ${PYDND_INTEGRATION_TEST_PATH} -v --cov=app --cov-report=html:${PYDND_INTEGRATION_COVERAGE_PATH} && open ${PYDND_INTEGRATION_COVERAGE_PATH}/index.html

################################################################################
# Utility
################################################################################

# Load in seed data -> source, dnd_class, spell, spell-to-class
.PHONY: pydnd-load-seeds
pydnd-load-seeds:
	cd pydnd && poetry run python3 scripts/load_seeds.py

.PHONY: reset-poetry
reset-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall && curl -sSL https://install.python-poetry.org | python3 -

# CREATE REVISION
# poetry run alembic revision --autogenerate -m "init"
