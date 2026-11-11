"""Backward-compatible facade; use parser_benchmark for new code."""
from parser_benchmark import BenchmarkResult,benchmark_parser,compare_parsers
__all__=["BenchmarkResult","benchmark_parser","compare_parsers"]
