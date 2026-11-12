def create_conversation(client, max_turns=2):
    response = client.post("/api/v1/conversations", json={
        "system_prompt": "You are helpful.", "max_turns": max_turns})
    assert response.status_code == 201
    return response.json()["id"]

def test_create_append_and_read_history(client):
    cid = create_conversation(client)
    user = client.post(f"/api/v1/conversations/{cid}/messages/user", json={"content": "Hello"})
    assistant = client.post(f"/api/v1/conversations/{cid}/messages/assistant", json={"content": "Hi"})
    assert user.status_code == assistant.status_code == 201
    result = client.get(f"/api/v1/conversations/{cid}").json()
    assert [m["role"] for m in result["messages"]] == ["user", "assistant"]

def test_requires_assistant_before_next_user(client):
    cid = create_conversation(client)
    url = f"/api/v1/conversations/{cid}/messages/user"
    assert client.post(url, json={"content": "first"}).status_code == 201
    assert client.post(url, json={"content": "second"}).status_code == 409

def test_bounded_history_removes_oldest_complete_turn(client):
    cid = create_conversation(client, max_turns=1)
    for n in range(2):
        client.post(f"/api/v1/conversations/{cid}/messages/user", json={"content": f"Q{n}"})
        client.post(f"/api/v1/conversations/{cid}/messages/assistant", json={"content": f"A{n}"})
    items = client.get(f"/api/v1/conversations/{cid}").json()["messages"]
    assert [m["content"] for m in items] == ["Q1", "A1"]

def test_not_found_and_pagination(client):
    assert client.get("/api/v1/conversations/missing").status_code == 404
    cid = create_conversation(client)
    client.post(f"/api/v1/conversations/{cid}/messages/user", json={"content": "Q"})
    client.post(f"/api/v1/conversations/{cid}/messages/assistant", json={"content": "A"})
    page = client.get(f"/api/v1/conversations/{cid}?limit=1&offset=1").json()
    assert len(page["messages"]) == 1 and page["messages"][0]["role"] == "assistant"

def test_clear_and_delete(client):
    cid = create_conversation(client)
    client.post(f"/api/v1/conversations/{cid}/messages/user", json={"content": "Q"})
    client.post(f"/api/v1/conversations/{cid}/messages/assistant", json={"content": "A"})
    assert client.delete(f"/api/v1/conversations/{cid}/messages").status_code == 204
    assert client.get(f"/api/v1/conversations/{cid}").json()["messages"] == []
    assert client.delete(f"/api/v1/conversations/{cid}").status_code == 204
    assert client.get(f"/api/v1/conversations/{cid}").status_code == 404

def test_unknown_fields_are_rejected(client):
    response = client.post("/api/v1/conversations", json={
        "system_prompt": "system", "unexpected": True})
    assert response.status_code == 422
