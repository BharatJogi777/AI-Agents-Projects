import pytest
from app.messages import SlackSearch

class Response:
    status_code=200
    def json(self): return {"ok":True,"messages":{"matches":[{"channel":{"name":"ops"},"user":"U1","text":"worker is healthy","ts":"123.4"}]}}
class Client:
    def get(self,*a,**k): return Response()

def test_search_maps_messages():
    result=SlackSearch(Client(),"xoxb-test").search("worker")
    assert result[0].channel=="ops" and result[0].text=="worker is healthy"

def test_rejects_unbounded_or_empty_query():
    with pytest.raises(ValueError): SlackSearch(Client(),"xoxb-test").search("")
    with pytest.raises(ValueError): SlackSearch(Client(),"xoxb-test").search("x",limit=101)

def test_rejects_bad_token():
    with pytest.raises(ValueError): SlackSearch(Client(),"bad").search("x")
