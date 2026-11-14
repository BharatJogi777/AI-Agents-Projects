"""Structure market observations and calculate transparent descriptive metrics."""
from dataclasses import dataclass
@dataclass(frozen=True)
class MarketSnapshot:
    observation_count: int
    segment_totals: tuple[tuple[str,float],...]
    average_price: float | None
    caveats: tuple[str,...]
def summarize_market(*, observations: list[dict]) -> MarketSnapshot:
    if not isinstance(observations,list): raise ValueError("observations must be a list")
    totals={}; prices=[]
    for item in observations:
        if not isinstance(item,dict) or not isinstance(item.get("segment"),str) or not item["segment"].strip(): raise ValueError("each observation needs a segment")
        size=item.get("market_size")
        if not isinstance(size,(int,float)) or isinstance(size,bool) or size<0: raise ValueError("market_size must be non-negative")
        totals[item["segment"].strip()]=totals.get(item["segment"].strip(),0.0)+float(size)
        price=item.get("price")
        if price is not None:
            if not isinstance(price,(int,float)) or isinstance(price,bool) or price<0: raise ValueError("price must be non-negative or None")
            prices.append(float(price))
    caveats=("Descriptive summary of supplied observations only.","No sampling-bias or market-size validation is performed.")
    return MarketSnapshot(len(observations),tuple(sorted(totals.items())),round(sum(prices)/len(prices),2) if prices else None,caveats)
