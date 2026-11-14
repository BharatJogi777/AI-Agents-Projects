from app.policy_compare import compare_policies

def test_reports_added_removed_and_modified_sections():
    changes = compare_policies(before={"1":"A", "2":"B"}, after={"1":"A changed", "3":"C"})
    assert [(c.section_id, c.change) for c in changes] == [("1","modified"),("2","removed"),("3","added")]

def test_identical_documents_have_no_changes():
    assert compare_policies(before={"1":"same"}, after={"1":"same"}) == ()

def test_rejects_invalid_section_value():
    import pytest
    with pytest.raises(ValueError):
        compare_policies(before={"1": 4}, after={})
