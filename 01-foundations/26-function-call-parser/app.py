"""Backward-compatible facade; use function_calls for new code."""
from function_calls import FunctionCall,FunctionCallError,dispatch_function_call,parse_function_call
__all__=["FunctionCall","FunctionCallError","dispatch_function_call","parse_function_call"]
