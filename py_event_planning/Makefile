include ../makefiles/common.mk
include ../makefiles/container.mk
include ../makefiles/postgres.mk


CONTAINER_RUNNER=docker # e.g. podman or docker

ENV_FILE = .env

CONTAINER_IMAGE = ttrpg-api/py_event_planning
CONTAINER_IMAGE_NAME = ttrpg-api-event-planning
define CONTAINER_RUN_ARGS
--env-file $(ENV_FILE) -dit -p 8002:8002
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
	poetry run uvicorn --host=127.0.0.1 --port=8002 py_event_planning.main:app

compose-up:
	${CONTAINER_RUNNER} compose \
		-f deploy/docker-compose.yml \
		-f ../deploy/postgres/postgres.compose.yml \
		-f ../deploy/keycloak/keycloak.compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		up -d

compose-down:
	${CONTAINER_RUNNER} compose \
		-f deploy/docker-compose.yml \
		-f ../deploy/postgres/postgres.compose.yml \
		-p ${CONTAINER_PROJECT_NAME} \
		down

mkdocs-run:
	poetry run mkdocs serve --dev-addr=127.0.0.1:8102
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
.PHONY: load-seed-data podman-init obliterate-migration k8s-deploy-keycloak

# Load in seed data -> source, dnd_class, spell, spell-to-class
load-seed-data:
	poetry run python3 scripts/load_seeds.py

# CREATE REVISION
# poetry run alembic revision --autogenerate -m "init"

# TODO: remove
# temporary
podman-init:
	rm -rf ~/.local/share/containers/podman && rm -rf ~/.config/containers && podman machine init

obliterate-migration:
	echo "My grandfather's deck has no pathetic cards, Kaiba!"
	poetry run alembic downgrade -1 && rm -rf ~/projects/ttrpg/ttrpg-api/py_event_planning/migrations/versions/* && poetry run alembic revision --autogenerate -m "init" && poetry run alembic upgrade head

container-build-all:
	${CONTAINER_RUNNER} build --network=host -f deploy/Dockerfile -t py_event_planning -t latest --target development .
	${CONTAINER_RUNNER} build --network=host -f ../deploy/keycloak/Dockerfile -t keycloak -t latest .
	# no docker file for postgresql

k3d-create:
	k3d cluster create ttrpg

k3d-delete:
	k3d cluster delete ttrpg

k3d-load-image-all:
	k3d image import py_event_planning:latest -c ttrpg
	k3d image import keycloak:latest -c ttrpg
	# no docker file for postgresql

k3s-load-image-all:
	docker save py_event_planning:latest | sudo k3s ctr images import -
	docker save keycloak:latest | sudo k3s ctr images import -
	# no docker file for postgresql

k8s-deploy-all-old:
	# PostgreSQL
	# kubectl apply -f ../deploy/postgres/master-pvc.deployment.yml
	kubectl apply -f ../deploy/postgres/keycloak.init.deployment.yml
	kubectl apply -f ../deploy/postgres/master.deployment.yml
	# kubectl apply -f ../deploy/postgres/replica-pvc.deployment.yml
	kubectl apply -f ../deploy/postgres/replica.deployment.yml
	# keycloak
	openssl req -subj '/CN=test.keycloak.org/O=Test Keycloak./C=US' -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
	kubectl create secret tls example-tls-secret --cert certificate.pem --key key.pem
	kubectl create secret generic keycloak-db-secret \
		--from-literal=username=admin \
		--from-literal=password=admin
	kubectl apply -f ../deploy/keycloak/deployment.yml
	# FastAPI
	kubectl apply -f ./deploy/deployment.yml

k8s-deploy-keycloak-initial:
	# create TLS cert
	openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout auth-tls.key -out auth-tls.crt -subj "/CN=auth.localtest.me/O=hotel"
	# kubectl delete secret tls auth-tls-secret
	kubectl create secret tls auth-tls-secret --key auth-tls.key --cert auth-tls.crt
	# deploy Keycloak cluster
	# kubectl apply -f ../deploy/keycloak/kc.service.yml
	# kubectl apply -f ../deploy/keycloak/kc.deployment.yml
	# # create HTTPS ingress for Keycloak
	# kubectl apply -f ../deploy/keycloak/kc.ingress.yml

k8s-deploy-keycloak:
	# deploy Keycloak cluster
	kubectl apply -f ../deploy/keycloak/kc.service.yml
	kubectl apply -f ../deploy/keycloak/kc.deployment.yml
	# create HTTPS ingress for Keycloak
	kubectl apply -f ../deploy/keycloak/kc.ingress.yml

k8s-deploy-all:
	# PostgreSQLd
	kubectl apply -f ../deploy/postgres/keycloak.init.deployment.yml
	kubectl apply -f ../deploy/postgres/master.service.yml
	kubectl apply -f ../deploy/postgres/master.deployment.yml
	kubectl apply -f ../deploy/postgres/replica.service.yml
	kubectl apply -f ../deploy/postgres/replica.deployment.yml
	# keycloak
	make k8s-deploy-keycloak
	# FastAPI
	kubectl apply -f ./deploy/service.yml
	kubectl apply -f ./deploy/deployment.yml

k8s-purge-all:
	kubectl delete all --all --all-namespaces
	kubectl delete secrets --all --all-namespaces
	kubectl delete configmap --all --all-namespaces
	kubectl delete pvc --all --all-namespaces
	kubectl delete pv --all
	# kubectl delete crd --all
	# kubectl delete serviceaccount --all --all-namespaces
	# kubectl delete networkpolicy --all --all-namespaces

k3s-restart:
	sudo systemctl restart k3s
