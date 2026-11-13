from dataclasses import dataclass
@dataclass(frozen=True)
class Offer:
    site:str
    item:str
    price:float
    currency:str
    availability:str
def compare_offers(offers:list[Offer])->list[dict]:
    if not offers: raise ValueError("at least one offer is required")
    if len({o.currency.strip().upper() for o in offers})!=1: raise ValueError("convert currencies using a trusted rate before comparison")
    for o in offers:
        if not o.site.strip() or not o.item.strip() or o.price<0 or not o.availability.strip(): raise ValueError("offer fields must be complete and price non-negative")
    return [{"site":o.site,"item":o.item,"price":o.price,"currency":o.currency.upper(),"availability":o.availability} for o in sorted(offers,key=lambda x:x.price)]
