

.PHONY: common-reset-poetry
common-reset-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall && curl -sSL https://install.python-poetry.org | python3 -
