import pytest
from app.issues import JiraIssues

class Response:
    status_code=200
    def json(self): return {"key":"OPS-12","fields":{"summary":"Restart worker","status":{"name":"Open"},"issuetype":{"name":"Task"}}}
class Client:
    def get(self,url,*,headers,params): self.url=url; return Response()

def test_maps_jira_issue():
    issue=JiraIssues(Client(),"https://example.atlassian.net","agent@example.com","token").get_issue("OPS-12")
    assert issue.key=="OPS-12" and issue.status=="Open"

def test_rejects_invalid_key():
    with pytest.raises(ValueError):
        JiraIssues(Client(),"https://example.atlassian.net","a","t").get_issue("../admin")

def test_requires_https():
    with pytest.raises(ValueError): JiraIssues(Client(),"http://example.com","a","t")
