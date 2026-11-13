"""Conservative guard for single-statement read-only SQL."""
import re

_FORBIDDEN=re.compile(r"\b(insert|update|delete|merge|drop|alter|create|truncate|grant|revoke|copy|call|do)\b",re.I)
def validate_read_query(sql: str)->str:
    query=sql.strip()
    if not query or len(query)>20_000:
        raise ValueError("query is empty or too long")
    if ";" in query.rstrip(";"):
        raise ValueError("only one SQL statement is allowed")
    normalized=query.rstrip(";").strip()
    if not re.match(r"^(select|with)\b",normalized,re.I):
        raise PermissionError("only SELECT or WITH queries are allowed")
    if _FORBIDDEN.search(normalized):
        raise PermissionError("query contains a forbidden operation")
    if "--" in normalized or "/*" in normalized or "*/" in normalized:
        raise ValueError("SQL comments are not accepted")
    return normalized
