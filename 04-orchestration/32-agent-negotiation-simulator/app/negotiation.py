"""Bounded alternating-offer negotiation simulator."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Offer:
    proposer: str
    amount: float

@dataclass(frozen=True)
class NegotiationResult:
    agreement: bool
    amount: float | None
    rounds: int
    reason: str

def negotiate(parties: dict[str, tuple[float, float]], max_rounds: int = 10) -> NegotiationResult:
    """Parties map name to (reservation_value, opening_offer); values are normalized."""
    if len(parties) != 2 or max_rounds < 1:
        raise ValueError("exactly two parties and positive max_rounds are required")
    names = sorted(parties)
    for reservation, opening in parties.values():
        if reservation < 0 or opening < 0:
            raise ValueError("values cannot be negative")
    # Buyer reservation is a maximum; seller reservation is a minimum.
    buyer, seller = parties[names[0]], parties[names[1]]
    ceiling, floor = buyer[0], seller[0]
    if floor > ceiling:
        return NegotiationResult(False, None, 0, "reservation ranges do not overlap")
    offer = buyer[1]
    for round_no in range(1, max_rounds + 1):
        if floor <= offer <= ceiling:
            return NegotiationResult(True, offer, round_no, "offer accepted within both reservation limits")
        # Alternate a midpoint counteroffer, converging without exceeding either reservation.
        offer = (max(floor, min(offer, ceiling)) + (floor if offer > ceiling else ceiling)) / 2
    return NegotiationResult(False, None, max_rounds, "round limit reached")
