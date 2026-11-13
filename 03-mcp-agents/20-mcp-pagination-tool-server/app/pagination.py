"""Bounded deterministic pagination over an in-memory sequence."""
from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar
T=TypeVar("T")

@dataclass(frozen=True)
class Page(Generic[T]):
    items: list[T]
    offset: int
    limit: int
    total: int
    has_more: bool

def paginate(items: Sequence[T], *, offset: int=0, limit: int=20, max_limit: int=100) -> Page[T]:
    if offset < 0:
        raise ValueError("offset cannot be negative")
    if limit < 1 or max_limit < 1 or limit > max_limit:
        raise ValueError("limit must be between 1 and max_limit")
    total=len(items)
    result=list(items[offset:offset+limit])
    return Page(result,offset,limit,total,offset+len(result)<total)
