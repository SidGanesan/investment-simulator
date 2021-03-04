from dataclasses import dataclass
from enum import Enum
from pandas import Series


class AssetClass(Enum):
    CASH = "cash"
    NZDEBT = "nz_debt"
    NZPROPERTY = "nz_property"
    GBLDEBT = "global_debt"
    NZEQUITY = "nz_equity"
    AUSEQUITY = "aus_equity"
    GBLEQUITY = "global_equity"
    ALTS = "alt_strategies"


@dataclass(frozen=True)
class AssetAllocation:
    """
    Value Object for Asset Allocation
    """

    asset_class: str
    weighting: float

    @property
    def annual_return(self) -> float:
        return asset_returns[self.asset_class]


asset_returns = Series(
    {
        "cash": 0.037,
        "nz_debt": 0.051,
        "nz_equity": 0.085,
        "aus_equity": 0.089,
        "global_equity": 0.078,
        "nz_property": 0.075,
        "alt_strategies": 0.075,
    }
)
