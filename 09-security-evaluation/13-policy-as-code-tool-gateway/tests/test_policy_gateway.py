from app.policy_gateway import authorize_tool_call

def test_default_deny_and_explicit_allow():
    assert not authorize_tool_call(principal="u",tool="db",action="write",policies=[])["allowed"]
    assert authorize_tool_call(principal="u",tool="db",action="read",policies=[{"principal":"u","tool":"db","action":"read","effect":"allow"}])["allowed"]

def test_deny_rule_wins():
    result = authorize_tool_call(principal="u",tool="db",action="read",policies=[{"principal":"*","tool":"*","action":"*","effect":"allow"},{"principal":"u","tool":"db","action":"read","effect":"deny"}])
    assert not result["allowed"]
