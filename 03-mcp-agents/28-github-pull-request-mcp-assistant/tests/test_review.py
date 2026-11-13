import pytest
from app.review import PullRequestReader

class Response:
    status_code=200
    def json(self): return {"number":7,"title":"Improve retry","state":"open","html_url":"https://github.com/acme/api/pull/7"}
class Client:
    def get(self,url,*,headers): self.url=url; return Response()

def test_reads_pull_request_without_mutation():
    client=Client()
    pr=PullRequestReader(client,"secret").get("acme","api",7)
    assert pr.number==7 and pr.state=="open"
    assert client.url.endswith("/pulls/7")

def test_invalid_number_rejected():
    with pytest.raises(ValueError): PullRequestReader(Client(),"x").get("a","b",0)

def test_api_failure_is_not_hidden():
    client=Client()
    class Failed:
        status_code=404
    client.get=lambda *a,**k: Failed()
    with pytest.raises(RuntimeError): PullRequestReader(client,"x").get("a","b",7)
