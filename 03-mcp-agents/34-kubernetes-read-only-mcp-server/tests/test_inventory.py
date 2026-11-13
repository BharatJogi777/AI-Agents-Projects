from types import SimpleNamespace as NS

import pytest
from app.inventory import list_pods, pod_summary


def pod(name="api", phase="Running", restarts=2):
    return NS(metadata=NS(name=name, namespace="default"),
              status=NS(phase=phase, container_statuses=[NS(restart_count=restarts)]),
              spec=NS(node_name="worker-1"))


class API:
    def list_namespaced_pod(self, **kwargs):
        assert kwargs == {"namespace": "default", "limit": 1}
        return NS(items=[pod()])


def test_pod_summary():
    assert pod_summary(pod())["restarts"] == 2


def test_list_pods_uses_namespace_and_limit():
    assert list_pods(API(), "default", 1)[0]["name"] == "api"


def test_bad_limit_rejected():
    with pytest.raises(ValueError):
        list_pods(API(), "default", 0)
