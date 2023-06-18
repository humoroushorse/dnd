include ../makefiles/common.mk
include ../makefiles/docker.mk
include ../makefiles/postgres.mk

ENV_FILE = .env

DOCKER_IMAGE = ttrpg-api/pydnd
define DOCKER_RUN_ARGS
--env-file $(ENV_FILE) -dit -p 8001:8001
endef

################################################################################
# App
################################################################################
.PHONY: alembic-upgrade
alembic-upgrade:
	# passing in override variable `db_override` to be read in `alembic/env.py`
	poetry run alembic upgrade head

.PHONY: db-up
db-up:
	make postgres-up
	sleep 2
	make alembic-upgrade
	make load-seed-data

.PHONY: start
start:
	# poetry env use python3 && poetry run uvicorn app.dnd.main:app
	poetry run uvicorn app.dnd.main:app

.PHONY: mkdocs
mkdocs:
	poetry run mkdocs serve --dev-addr=0.0.0.0:8001

################################################################################
# Testing
################################################################################
TEST_PATH=app/dnd/tests
COVERAGE_PATH=htmlcov/pydnd
INTEGRATION_TEST_PATH=${TEST_PATH}/integration
INTEGRATION_COVERAGE_PATH=${COVERAGE_PATH}/integration
UNIT_TEST_PATH=${TEST_PATH}/unit
UNIT_COVERAGE_PATH=${COVERAGE_PATH}/unit

# passing in override variable `db_override` to be read in `alembic/env.py`
.PHONY: alembic-upgrade-testing
alembic-upgrade-testing:
	poetry run alembic -x db_override=${DOCKER_PG_TEST_CONN} upgrade head

.PHONY: test-unit
test-unit:
	poetry run pytest ${UNIT_TEST_PATH} -v --cov=app

.PHONY: test-unit-html
test-unit-html:
	poetry run pytest ${UNIT_TEST_PATH} -v --cov=app --cov-report=html:${UNIT_COVERAGE_PATH} && open ${UNIT_COVERAGE_PATH}/index.html

# For integration: create clean database and then run integration tests
.PHONY: test-integration
test-integration:
	make postgres-up-testing
	sleep 2
	make alembic-upgrade-testing
	# run the tests and even if they fail, destroy the docker container
	poetry run pytest ${INTEGRATION_TEST_PATH} --seed="${SEED}" --skip-d20="${SKIP_D20}" --maxfail=1 -v --cov=app || echo "continuing even if error"
	make postgres-down-testing

.PHONY: test-integration-html
test-integration-html:
	poetry run pytest ${INTEGRATION_TEST_PATH} -v --cov=app --cov-report=html:${INTEGRATION_COVERAGE_PATH} && open ${INTEGRATION_COVERAGE_PATH}/index.html

################################################################################
# Utility
################################################################################

# Load in seed data -> source, dnd_class, spell, spell-to-class
.PHONY: load-seed-data
load-seed-data:
	poetry run python3 scripts/load_seeds.py

# CREATE REVISION
# poetry run alembic revision --autogenerate -m "init"
