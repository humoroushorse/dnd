# How to Update Python Version

When updating the python version you have to do a few things

1. update brew/pyenv
   1. `brew doctor`
   2. `brew update`
   3. `brew upgrade pyenv`
   4. [optional] you may have to do this a few times...
2. install your python version with pyenv
   1. check versions: `pyenv install --list | grep 3.x`
   2. install version: `pyenv install 3.x.x`
   3. set global: `pyenv global 3.x.x`
   4. verify install: `pyenv versions`
   5. [optional] you may have to restart your terminal
3. set the python version in each of the python projects
   1. `poetry env use 3.x`
   2. update version in each `pyproject.toml`
   3. update version in each `.pre-commit-config.yaml`
4. update project versions
   1. `poetry update`
   2. `poetry run pre-commit autoupdate`
5. update VS Code interpreter
   1. see [vscode_set_python_interpreter.md](./vscode_set_python_interpreter.md)
