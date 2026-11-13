"""Tool argument fuzz tester: deterministic evaluation helper."""

def generate_cases(*, schema: dict[str, object]):
        if not isinstance(schema, dict) or not schema:
            raise ValueError("schema must be a non-empty mapping")
        cases = []
        for field, rule in schema.items():
            if not isinstance(field, str) or not isinstance(rule, dict):
                raise ValueError("each field must map to a rule dictionary")
            kind = rule.get("type")
            cases.extend([{"field": field, "value": None, "case": "null"}, {"field": field, "value": [], "case": "empty-list"}, {"field": field, "value": {}, "case": "object-instead-of-scalar"}])
            if kind == "string": cases.extend([{"field":field,"value":"\u0000","case":"null-byte"},{"field":field,"value":"x"*4096,"case":"oversized-string"}])
            elif kind == "integer": cases.extend([{"field":field,"value":-1,"case":"negative"},{"field":field,"value":10**100,"case":"huge-integer"}])
            elif kind == "number": cases.extend([{"field":field,"value":float("nan"),"case":"nan"},{"field":field,"value":float("inf"),"case":"infinity"}])
            else: raise ValueError(f"unsupported schema type for {field}")
        return cases
