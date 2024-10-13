# TTRPG API
Welcome to the TTRPG API!

## Localhost
Localhost changes based on where you run it from
* CLI: 127.0.0.1
* Docker: 0.0.0.0

## Port Space Allocation
As a source of truth please refer to this [confluence page](https://ian-kirkpatrick.atlassian.net/wiki/spaces/DND/pages/3211317/Local).

| Project Name    | Description   | Ports       |
|-----------------|---------------|-------------|
| Grafana         | service       | 3000        |
| UI              | ui ports      | 4xxx        |
| registry        | containers    | 5001        |
| API             | api ports     | 8xxx - 8100 |
| API DOCS        | api doc ports | 81xx - 8200 |
| OPA             | opa ports     | 82xx - 8300 |
| Prometheus      | service       | 9090        |

## Port Ledger
| Project Name    | Description | Ports       |
|-----------------|-------------|-------------|
| postgres        | DB          | 5432        |
| postgres (test) | Test DB     | 5433        |
| keycloak        | auth        | 8080        |
| pydnd           | FastAPI     | 8001        |
| pydnd: mkdocs   | docs        | 8201        |
| pydnd: opa      | opa         | 8301        |  TODO - reserved, implement (update, remove in favor of keycloak)
| pydnd           | FastAPI     | 8002        |
| pydnd: mkdocs   | docs        | 8202        |


## Projects

### pydnd
This is a FastAPI repository
- see `./pydnd/docs`

For further documentation run
```shell
make pydnd-mkdocs
```
And then go to `http://localhost:8001`
___
## Project Technologies Et Cetera
### Poetry
Here's a link to the [Poetry Docs](https://python-poetry.org/docs/cli/)

poetry was chosen as the package management solution
* article 1 (why poetry): https://hackersandslackers.com/python-poetry-package-manager/
* article 2 (general setup): https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1
* article 2.5 (vs code integration): https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-2

### FastAPI Setup
* In general it follows [this GitHub skeleton project](https://github.com/skb1129/fastapi-boilerplate/tree/master/app)
  * This is a smaller, more lightweight version of [tiangolo's skeleton project](https://github.com/tiangolo/full-stack-fastapi-postgresql) (the creator of FastAPI made a full stack project, this project is just the backend part of his project without the security stuff)

## TODO
- in `./pylintrc` investigate removing the disables for [consider-using-with, broad-except]
- investigate if I want to use UOW pattern or just Repository pattern
