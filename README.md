# Investment-Simulator
Library for simulating a persons investment portfolio over time based on risk and return. Focusing of modeling Stochastic methods such as Monte
 Carlo Simulations and implemented using functional styled python.

## Development
Dependencies managed using `poetry` and can be installed using `poetry install`

### Git Hooks
This repository uses git hooks for; formatting using black, debug checks, and running tests. This will auto format any commits to a forced styling
 using black, check for debug statements, and block commits where tests fail.

### Tests
Testing is done in `pytest` and can be initiated using:
```shell script
poetry run python -m pytest
```

## Done
* Monte Carlo simulation for an portfolio based on asset weightings and returns
* Git hooks for; formatting using black, debug checks, and running tests.

## Todo
* Test Coverage
* Functional input for contributions to allow modeling of NZ Kiwisaver scheme
* Back solving probabilities of achieving a fixed goal
* Actuarial based formulae and functions for modeling investments
