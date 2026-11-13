import asyncio
import pytest
from app.adapter import RestAdapter


def test_rejects_unallowlisted_route():
    client = RestAdapter("http://localhost:8000", "", {"/v1/services"})
    with pytest.raises(PermissionError):
        asyncio.run(client.get("/admin"))


def test_rejects_path_traversal_route():
    with pytest.raises(ValueError):
        RestAdapter("http://localhost:8000", "", {"/../admin"})


def test_requires_explicit_routes():
    with pytest.raises(ValueError):
        RestAdapter("http://localhost:8000", "", set())
