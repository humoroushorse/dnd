COMMON_REPOSITORY_ROOT=~/projects/ttrpg/ttrpg-api

.PHONY: common-poetry-reset
common-poetry-reset:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall && curl -sSL https://install.python-poetry.org | python3 -
