import pytest
from app.issues import GitHubIssues

class Response:
    status_code=200
    def json(self):
        return [{"number":3,"title":"Bug","state":"open","html_url":"https://github.com/o/r/issues/3"},
                {"number":4,"title":"PR","state":"open","html_url":"https://github.com/o/r/pull/4","pull_request":{}}]
class Client:
    def __init__(self): self.call=None
    def get(self,url,*,headers,params):
        self.call=(url,headers,params); return Response()

def test_lists_issues_and_skips_pull_requests():
    client=Client()
    issues=GitHubIssues(client,"token").list_issues("o","r")
    assert len(issues)==1 and issues[0].number==3
    assert client.call[1]["Authorization"]=="Bearer token"

def test_invalid_limit_rejected():
    with pytest.raises(ValueError): GitHubIssues(Client(),"token").list_issues("o","r",limit=101)

def test_non_200_is_error():
    client=Client()
    class Failed:
        status_code=403
        def json(self): return {}
    client.get=lambda *a,**k: Failed()
    with pytest.raises(RuntimeError): GitHubIssues(client,"token").list_issues("o","r")
