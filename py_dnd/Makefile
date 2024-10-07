include ../makefiles/common.mk
include ../makefiles/container.mk
include ../makefiles/postgres.mk


CONTAINER_RUNNER=docker # e.g. podman or docker

ENV_FILE = .env

CONTAINER_IMAGE = ttrpg-api/py_event_planning
CONTAINER_IMAGE_NAME = dnd-api
define CONTAINER_RUN_ARGS
--env-file $(ENV_FILE) -dit -p 8001:8001
endef

################################################################################
# App
################################################################################
.PHONY: alembic-upgrade db-up run compose-up compose-down mkdocs-run

alembic-upgrade:
	# passing in override variable `db_override` to be read in `migrations/env.py`
	poetry run alembic upgrade head

db-up:
	make postgres-up
	sleep 2
	make alembic-upgrade
	make load-seed-data

run:
	# poetry env use python3 && poetry run uvicorn py_event_planning.main:app
	poetry run uvicorn --host=127.0.0.1 --port=8001 py_event_planning.main:app

compose-up:
	${CONTAINER_RUNNER} compose \
		-f image/docker-compose.yml \
		-f ../image/postgres.compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		up -d

compose-down:
	${CONTAINER_RUNNER} compose \
		-f image/docker-compose.yml \
		-f ../image/postgres.compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		down

mkdocs-run:
	poetry run mkdocs serve --dev-addr=127.0.0.1:8101

################################################################################
# Testing
################################################################################
.PHONY: alembic-upgrade-testing test-unit test-unit-html test-integration test-integration-html

TEST_PATH=app/dnd/tests
COVERAGE_PATH=htmlcov/py_event_planning
INTEGRATION_TEST_PATH=${TEST_PATH}/integration
INTEGRATION_COVERAGE_PATH=${COVERAGE_PATH}/integration
UNIT_TEST_PATH=${TEST_PATH}/unit
UNIT_COVERAGE_PATH=${COVERAGE_PATH}/unit

# passing in override variable `db_override` to be read in `migrations/env.py`
alembic-upgrade-testing:
	pwd
	poetry run alembic -x db_override=${CONTAINER_POSTGRES_TEST_CONN} upgrade head

test-unit:
	poetry run pytest ${UNIT_TEST_PATH} -v --cov=app

test-unit-html:
	poetry run pytest ${UNIT_TEST_PATH} -v --cov=app --cov-report=html:${UNIT_COVERAGE_PATH} && open ${UNIT_COVERAGE_PATH}/index.html

# For integration: create clean database and then run integration tests
test-integration:
	make postgres-up-testing
	sleep 2
	make alembic-upgrade-testing
	# run the tests and even if they fail, destroy the container
	poetry run pytest ${INTEGRATION_TEST_PATH} --seed="${SEED}" --skip-d20="${SKIP_D20}" --maxfail=1 -v --cov=app || echo "continuing even if error"
	make postgres-down-testing

test-integration-html:
	poetry run pytest ${INTEGRATION_TEST_PATH} -v --cov=app --cov-report=html:${INTEGRATION_COVERAGE_PATH} && open ${INTEGRATION_COVERAGE_PATH}/index.html

################################################################################
# Utility
################################################################################
.PHONY: load-seed-data podman-init

# Load in seed data -> source, dnd_class, spell, spell-to-class
load-seed-data:
	poetry run python3 scripts/load_seeds.py

# CREATE REVISION
# poetry run alembic revision --autogenerate -m "init"

# TODO: remove
# temporary
podman-init:
	rm -rf ~/.local/share/containers/podman && rm -rf ~/.config/containers && podman machine init
