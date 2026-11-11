"""Compatibility facade. New code should import memory_retrieval."""
from memory_retrieval import Memory,RankedMemory,retrieve,retrieve_ranked
__all__=["Memory","RankedMemory","retrieve","retrieve_ranked"]
