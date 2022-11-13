# dnd

## Projects

### pydnd
This is a FastAPI repository
- see `./pydnd/docs`

For further documentation run
```shell
make pydnd-mkdocs
```
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
- in `./pydnd/docs` finish pointing references for all modules
- tracing && logging for python
- /bulk endpoints return Any right now, create type for that
- investigate if I want to use UOW pattern or just Repository pattern
- change `__init__.py` imports for say schemas (maybe more) -> less 'flattening'
- convert print statements to logging (search for prints with noqa T001)
