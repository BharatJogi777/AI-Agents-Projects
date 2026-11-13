from app.diagnostics import hit_rate,sanitize_info

def test_sanitizes_info_allowlist():
    result=sanitize_info({"redis_version":"7.2","connected_clients":3,"requirepass":"secret","unexpected":True})
    assert result=={"redis_version":"7.2","connected_clients":3}

def test_hit_rate_and_empty_counters():
    assert hit_rate({"keyspace_hits":8,"keyspace_misses":2})==0.8
    assert hit_rate({"keyspace_hits":0,"keyspace_misses":0}) is None
    assert hit_rate({}) is None
