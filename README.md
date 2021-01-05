# Investment-Simulator

Library for simulating a persons investment portfolio over time based on risk and return. This library makes use of [Markowitz/Modern Portfolio Theory
](https://www.investopedia.com/terms/m/modernportfoliotheory.asp "Modern Portfolio Theory") to model portfolio return and risk using the covariance
 of assets held. Focusing of modeling Stochastic methods such as Monte Carlo Simulations and implemented using functional styled python.

---

## Usage
### Portfolio Simulation
Basic Usage:
```python
from investment_simulator.portfolio_simulation import monte_carlo_sim

asset_weights = [0.5, 0.5]
asset_returns = [0.1, 0.1]
covariance = [[1.0, 0.0], [0.0, 1.0]]
steps = 10

result = monte_carlo_sim(asset_weights, asset_returns, covariance, steps)
```

The result is a [Value Object/Frozen Data Class](https://docs.python.org/3/library/dataclasses.html "Data Classes") containing the mean outcome of
 1000 simulations over 10 years steps, as well as the calculated risk and return of the modelled portfolio.
 ```python
SimulationResults(
    portfolio_return=0.10000000000000009,
    portfolio_risk=0.7071067811865476,
    simulation_mean=[1.0, 1.080889920462147, 1.1770098655116579, 1.372350014835664, 1.7036261053980901,
                     1.7926598558102225, 1.9825789493200046, 2.621924082582044, 3.200699630098704, 3.2614308258392573, 4.211555444216132],
    simulation_std=[0.0, 0.8151713183859045, 1.407052616672628, 3.0336270877135734, 4.8721084117880755,
                    4.915923260576842, 6.394237270341292, 13.456266947236522, 24.550547468886933, 29.54050507961563, 42.62272966366064],
    x_max=10,
    y_max=46.834285107876774
)
```

### Contribution Functions
The simulation has the ability to add annual contributions to the portfolio uniformly across simulations. The contribution function should take the
 time step as an input and return a contribution amount. For example a function could be defined as:
```python
def continuous_contributions(
    initial_contribution: float,
    contribution_growth: float = 0.0
) -> Callable:
    def inner(step: int) -> float:
        return initial_contribution *  (1 +contribution_growth) ** step

    return inner
```

Where a function`continuous_contributions` is defined as the default contributions function. Such that there is the `initial_contribution` added to
 to a portfolio in the simulation which grows annually at a rate of `contributuion_growth` compounded by the step.
 
---

## Development
Dependencies managed using `poetry` and can be installed using `poetry install`

### Git Hooks
This repository uses git hooks for; formatting using black, debug checks, and running tests. This will auto format any commits to a forced styling
 using black, check for debug statements, and block commits where tests fail. Pre Commit can be run using `pre-commit run --all-files` in terminal to
  check your changes before committing if preferred.

### Tests
Testing is done in `pytest` and can be initiated using:
```shell script
poetry run python -m pytest
```
---

## Done
* Monte Carlo simulation for an portfolio based on asset weightings and returns.
* Git hooks for; formatting using black, debug checks, and running tests.

## Todo
* Test Coverage
* More contribution functions to support usage.
* Tax calculation and input to better model income based contribution functions.
* Back solving probabilities of achieving a fixed goal.
* Actuarial based formulae and functions for modeling investments.
