# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/
ARG PYTHON_DOCKER_IMAGE=python:3.13.0-alpine

################################################################################
# python-base
#    Creating a python base with shared environment variables
################################################################################
FROM $PYTHON_DOCKER_IMAGE AS python-base

WORKDIR /tmp

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on
    # PIP_DEFAULT_TIMEOUT=100 \
    # POETRY_HOME="/opt/poetry" \
    # POETRY_VIRTUALENVS_IN_PROJECT=true \
    # POETRY_NO_INTERACTION=1 \
    # PYSETUP_PATH="/opt/pysetup" \
    # VENV_PATH="/opt/pysetup/.venv"

# Poetry
RUN pip install poetry
COPY . .
# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

################################################################################
# builder-base
#    'builder-base' stage is used to build dependencies
################################################################################
FROM python-base AS builder-base

# RUN buildDeps="build-essential" \
#     && apt-get update \
#     && apt-get install --no-install-recommends -y \
#         curl \
#         vim \
#     && apt-get install -y --no-install-recommends $buildDeps \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

RUN poetry build --format wheel

################################################################################
# development
#    'development' stage installs all dev deps and can be used to develop code.
#    For example using docker-compose to mount local volume under /app
################################################################################
# FROM python-base as development
FROM $PYTHON_DOCKER_IMAGE AS development

ENV FASTAPI_ENV=production
ENV FASTAPI_port=8001

WORKDIR /code

# COPY --from=builder-base /tmp/requirements.txt ./requirements.txt
# RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY --from=builder-base /tmp/dist/ /dist/
RUN pip install --no-cache-dir /dist/*.whl
# COPY . .

# poetry run uvicorn --reload --host=0.0.0.0 --port=8001 --app-dir=py_dnd main:app
# CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8001", "py_dnd.main:app"]
WORKDIR /
COPY --from=python-base /tmp/deploy/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE ${FASTAPI_port}
ENTRYPOINT [ "/docker-entrypoint.sh" ]

################################################################################
# lint (development)
#    'lint' stage runs black and isort
#    running in check mode means build will fail if any linting errors occur
################################################################################

FROM development AS lint
RUN black --config ./pyproject.toml --check app tests
RUN isort --settings-path ./pyproject.toml --recursive --check-only
CMD ["tail", "-f", "/dev/null"]

################################################################################
# test (development)
#    'test' stage runs our unit tests with pytest and
#    coverage.  Build will fail if test coverage is under 95%
################################################################################
FROM development AS test
RUN coverage run --rcfile ./pyproject.toml -m pytest ./tests
RUN coverage report --fail-under 95
