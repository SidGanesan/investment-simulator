# Investment-Simulator
Library for simulating a persons investment portfolio over time based on risk and return. Focusing of modeling Stochastic methods such as Monte
 Carlo Simulations and implemented using functional styled python.

## Usage
### Portfolio Simulation
Basic Usage
```python
from investment_simulator.portfolio_simulation import monte_carlo_sim

asset_weights = [0.5, 0.5]
asset_returns = [0.1, 0.1]
covariance = [[1.0, 0.0], [0.0, 1.0]]
steps = 10

result = monte_carlo_sim(asset_weights, asset_returns, covariance, steps)
```

### Contribution Functions
The simulation has the ability to add annual contributions to the portfolio uniformly across simulations. The contribution function should take the
 timestep as an input and return a contribution amount. For example a function could be defined as:
```python
def continuous_contributions(step: int) -> float:
    return 1_000 * (1.02) ** step
```

Where a function`continuous_contributions` could be defined, such that there was a `1_000` annual contribution and a growth of `0.02` for
 inflation each year, compounded by the step.

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
