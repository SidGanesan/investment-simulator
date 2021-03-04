from typing import Dict, Tuple, List

from investment_lambda.value_objects.asset_allocation import AssetAllocation


def construct_allocation(args):
    return AssetAllocation(asset_class=args["asset_class"], weighting=args["weighting"])


def build_portfolio(
    payload: List[Dict[str, float]]
) -> Tuple[Tuple[AssetAllocation, ...], Tuple[float, ...]]:
    return tuple(map(construct_allocation, payload)), tuple(
        map(lambda val: val.get("weighting", 0.0), payload)
    )


def get_asset_allocations(
    allocations: Dict,
) -> Tuple[Tuple[AssetAllocation, ...], Tuple[float, ...]]:
    portfolio = build_portfolio(allocations["payload"])
    return portfolio
