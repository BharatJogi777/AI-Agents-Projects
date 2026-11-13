from types import SimpleNamespace as NS

import pytest
from app.inventory import container_summary, list_containers


class Containers:
    def list(self, **kwargs):
        assert kwargs == {"all": False, "limit": 1}
        return [NS(short_id="abc", name="api", status="running",
                   attrs={"Config": {"Image": "nginx"}, "State": {"Status": "running"}})]


class Client:
    containers = Containers()


def test_container_summary():
    result = container_summary(Client.containers.list()[0])
    assert result["image"] == "nginx"
    assert result["name"] == "api"


def test_list_is_bounded_and_read_only():
    assert len(list_containers(Client(), False, 1)) == 1


def test_bad_limit_rejected():
    with pytest.raises(ValueError):
        list_containers(Client(), False, 0)
