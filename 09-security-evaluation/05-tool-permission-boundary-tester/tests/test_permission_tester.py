from app.permission_tester import check_tool_permissions

def test_default_deny_and_explicit_grant():
    result = check_tool_permissions(requests=[{"principal":"reader","tool":"search","action":"query"},{"principal":"reader","tool":"mail","action":"send"}], grants={"reader:search":["query"]})
    assert [x["allowed"] for x in result] == [True, False]

def test_rejects_incomplete_request():
    import pytest
    with pytest.raises(ValueError): check_tool_permissions(requests=[{"principal":"reader"}], grants={})
