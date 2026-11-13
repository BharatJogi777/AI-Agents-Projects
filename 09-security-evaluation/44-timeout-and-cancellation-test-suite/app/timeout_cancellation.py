"""Async deadline helper that propagates cancellation to the awaited operation."""
import asyncio
from typing import Awaitable,TypeVar
T=TypeVar("T")
async def run_with_timeout(operation:Awaitable[T],*,timeout_seconds:float)->T:
 if timeout_seconds<=0: raise ValueError("timeout_seconds must be positive")
 return await asyncio.wait_for(operation,timeout=timeout_seconds)
