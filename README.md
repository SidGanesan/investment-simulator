# Investment-Simulator

Library for simulating a persons investment portfolio over time based on risk and return. This library makes use of [Markowitz/Modern Portfolio Theory
](https://www.investopedia.com/terms/m/modernportfoliotheory.asp "Modern Portfolio Theory") to model portfolio return and risk using the covariance
 of assets held. Focusing of modeling Stochastic methods such as [Monte Carlo Simulations](https://corporatefinanceinstitute.com/resources/knowledge/modeling/monte-carlo-simulation/
 "Monte Carlo For Finance") and implemented using functional styled python.

---

## Table of Contents
- [Install](#install)
- [Usage](#usage)
  - [Portfolio Simulations](#portfolio simulations)
  - [Investment Goals](#investment-goals)
  - [Contribution Functions](#contribution-functions)
  - [Allocation Optimisation](#allocations-optimisation)
- [Contributing](#contributing)
- [License](#license)

---

## Install

Install from PyPi:
```
pip install investment-simulator
```
```
poetry add investment-simulator
```

## Usage
### Portfolio Simulations

The library offers the ability to simulate how a portfolio will grow over time in a stochastic way, showing the variance of possible outcomes based on
 asset allocations and how the assets are related to each other. The library requires the user to give the average annual return, asset weightings,
  the covariance between the assets, and number of steps in the simulation (investment horizon).

Basic usage:
```python
from investment_simulator.portfolios import growth_simulation

asset_weights = [0.5, 0.5]
asset_returns = [0.1, 0.1]
covariance = [[1.0, 0.0], [0.0, 1.0]]
steps = 10

growth_simulation(asset_weights, asset_returns, covariance, steps)
```

The result is a [Value Object/Frozen Data Class](https://docs.python.org/3/library/dataclasses.html "Data Classes") containing the mean outcome of
 1000 simulations over 10 years steps, as well as the calculated risk and return of the modelled portfolio.
 ```python
PortfolioResults(
    portfolio_return=0.10000000000000009,
    portfolio_risk=0.7071067811865476,
    simulation_mean=[1.0, 1.080889920462147, 1.1770098655116579, 1.372350014835664, 1.7036261053980901,
                     1.7926598558102225, 1.9825789493200046, 2.621924082582044, 3.200699630098704,
                     3.2614308258392573, 4.211555444216132],
    simulation_std=[0.0, 0.8151713183859045, 1.407052616672628, 3.0336270877135734, 4.8721084117880755,
                    4.915923260576842, 6.394237270341292, 13.456266947236522, 24.550547468886933,
                    29.54050507961563, 42.62272966366064],
)
```

### Investment Goals

The investment simulator also allows optionally for an investment goal to be input to calculate the likelihood of achieving it.
 This is done in the same growth function when the optional `investment_goal` parameter is input and non-zero. This causes the
  function to return an `InvestmentResults` object which inherits from `PortfolioResults`

For example; a person my want to save for a certain amount of money for retirement, where the simulation could be used to determine the percentage outcomes that
  reach the desired amount, as well what additional payments would be required so that the goal is likely to be achieved. Outcomes are assumed
   to be normally distributed and additional payments are to achieve a probability of 50% of achieving the goal. This is used as follows:
```python
from investment_simulator.portfolios import growth_simulation

asset_weights = [0.5, 0.5]
asset_returns = [0.1, 0.1]
covariance = [[1.0, 0.0], [0.0, 1.0]]
steps = 10
investment_goal = 2.5

growth_simulation(
        asset_weightings= asset_weights,
        annual_returns=asset_returns,
        covariance=covariance,
        steps=steps,
        investment_goal=investment_goal,
    )
```

The result of which is:
```python
InvestmentResults(
    portfolio_return=0.10000000000000009,
    portfolio_risk=0.022360679774997897,
    simulation_mean=[1.0, 1.0995099544525146, 1.210924506187439, 1.3327478170394897, 1.4653383493423462,
                     1.6140620708465576, 1.7742526531219482, 1.9512927532196045, 2.1460065841674805,
                     2.357496976852417, 2.5915284156799316],
    simulation_std=[0.0, 0.024642884731292725, 0.039426639676094055, 0.052822574973106384, 0.06663929671049118,
                   0.08260171860456467, 0.10066824406385422, 0.11744718253612518, 0.13588516414165497,
                   0.1578415483236313, 0.18211820721626282],
    goal=2.5,
    probability=0.6923691357161944,
    additional_savings=-0.0)
```
Where the person has approximately 70% probability of achieving their investment goal, and doesn't require any additional savings to improve their
 likelihood above 50%.

### Contribution Functions

The simulation has the ability to add annual contributions to the portfolio uniformly across simulations. The contribution function should take the
 time step as an input and return a contribution amount. For example a function could be defined as:
```python
def continuous_contributions(
    initial_contribution: float,
    contribution_growth: float = 0.0
) -> Callable[[int], float]:
    def inner(step: int) -> float:
        return initial_contribution *  (1 +contribution_growth) ** step

    return inner
```

Where a function`continuous_contributions` is defined as the default contributions function. Such that there is the `initial_contribution` added to
 to a portfolio in the simulation which grows annually at a rate of `contributuion_growth` compounded by the step.

---

### Allocations Optimisation

The library also offers the ability to optimise the allocations of a portfolio, determining the weightings of assets that provide the highest
 return for the lowest risk. This follows the concept of the [Efficient Portfolio Frontier](https://www.investopedia.com/terms/e/efficientfrontier.asp
 "Efficient Portfolio Frontier") by generating a series of random portfolios to build the curve, then maximising for the portfolio with the
  highest Sharpe Ratio.
```python
from investment_simulator.allocations import allocations_simulation

annual_returns = [0.1, 0.1]
covariance = [[0.001, 0.000], [0.000, 0.001]]
simulations = 10

allocations_simulation(annual_returns, covariance, simulations)
```

The result is a [Value Object(Frozen Data Class)](https://docs.python.org/3/library/dataclasses.html "Data Classes") containing the portfolio with
 the highest sharpe ratio score.
```python
AllocationResults(
    sharpe_ratio=4.020794467140073,
    annual_return=0.10000000000000009,
    risk=0.022383636053900476,
    weights=[0.52266234, 0.47733766]
)
```

---

## Maintainers

[@SidGanesan](https://github.com/jarden-sid)

---

## Contributing

Please contribute! [Look at the issues](https://github.com/jarden-sid/investment-simulator/issues).


### Development
Dependencies managed using `poetry` and can be installed using `poetry install`

#### Git Hooks
This repository uses git hooks for; formatting using black, debug checks, and running tests. This will auto format any commits to a forced styling
 using black, check for debug statements, and block commits where tests fail. Pre Commit can be run using `pre-commit run --all-files` in terminal to
  check your changes before committing if preferred.

#### Tests
Testing is done in `pytest` and can be initiated using:
```shell script
poetry run python -m pytest -v
```

### Done
* Monte Carlo simulation for an portfolio based on asset weightings and returns.
* Portfolio Simulation for optimal asset allocations
* Back solving probabilities of achieving a fixed goal.
* Git hooks for; formatting using black, debug checks, and running tests.
* Tax calculation and input to better model income based contribution functions.

### Todo
* Test Coverage
* More contribution functions to support usage.
* Actuarial based formulae and functions for modeling investments.
---

## License

MIT © 2016
