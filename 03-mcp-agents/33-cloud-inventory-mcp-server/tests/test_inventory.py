from app.inventory import list_inventory, summarize_instance


class Paginator:
    def __init__(self, pages):
        self.pages = pages

    def paginate(self, **kwargs):
        assert kwargs["PaginationConfig"]["MaxItems"] == 2
        return iter(self.pages)


class Client:
    def __init__(self, pages):
        self.pages = pages

    def get_paginator(self, operation):
        assert operation == "describe_instances"
        return Paginator(self.pages)


def test_summarize_instance_omits_unneeded_fields():
    result = summarize_instance({"InstanceId": "i-1", "State": {"Name": "running"}, "Secret": "omit"})
    assert result["instance_id"] == "i-1"
    assert "Secret" not in result


def test_inventory_is_bounded():
    client = Client([{"Reservations": [{"Instances": [
        {"InstanceId": "i-1", "State": {"Name": "running"}},
        {"InstanceId": "i-2", "State": {"Name": "stopped"}},
        {"InstanceId": "i-3", "State": {"Name": "running"}},
    ]}]}])
    assert len(list_inventory(client, "us-east-1", 2)) == 2


def test_invalid_limit_rejected():
    import pytest
    with pytest.raises(ValueError):
        list_inventory(Client([]), "us-east-1", 0)
