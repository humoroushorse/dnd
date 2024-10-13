# Testing

## Tooling
For testing we will do the following
* [pytest](https://docs.pytest.org/) our test runner
* [coverage.py](https://coverage.readthedocs.io/) for coverage and cool html reporting
* [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) fancy extension of coveraage.py essentially

## Running the tests

First: `cd ~/ttrpg/ttrpg-api`

___
### Unit
To simply run the tests for py_event_planning and see a simple cli report you can use the following:

```shell
make test-unit
```

If you want to generate a HTML report and open that in your browser you can run the following:

```shell
make test-unit-html
```

___
### Integration
Run integration
```shell
make test-integration
```
See HTML report
```shell
make test-integration-html
```
#### Debugging with random seeds
Integration tests run with random seeds.
On error you will see a message along the lines of `Running tests with seed: 1999154338096897425`

In this instance, to produce the same results, run the following
```shell
make test-integration SEED=1999154338096897425
```

#### the d20 roll test
There is a 1 in 20 chance you will fail the d20 test. This is D&D afterall.

If you want a failing d20 roll you can do
```shell
make test-integration SEED=5542828861354271048
```

To skip the d20 test (say for CICD) you can use `--skip-d20`
```shell
make test-integration SEED=5542828861354271048 SKIP_D20=True
```
_____
## Other Resources
* Here's a short [YouTube video by SBCODE](https://www.youtube.com/watch?v=7BJ_BKeeJyM) about test coverage in python
