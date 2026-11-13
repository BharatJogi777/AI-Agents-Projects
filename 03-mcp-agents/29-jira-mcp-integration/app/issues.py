"""Typed, read-only Jira issue lookup using an injected transport."""
from dataclasses import dataclass
from base64 import b64encode
from typing import Protocol

class Response(Protocol):
    status_code:int
    def json(self)->object: ...
class Client(Protocol):
    def get(self,url:str,*,headers:dict[str,str],params:dict[str,str])->Response: ...

@dataclass(frozen=True)
class JiraIssue:
    key:str
    summary:str
    status:str
    issue_type:str

class JiraIssues:
    def __init__(self,client:Client,base_url:str,email:str,token:str):
        if not base_url.startswith("https://") or not email.strip() or not token.strip():
            raise ValueError("HTTPS base URL, email, and token are required")
        self.client,self.base_url,self.email,self.token=client,base_url.rstrip("/"),email,token

    def get_issue(self,key:str)->JiraIssue:
        if not key or len(key)>64 or not all(c.isalnum() or c in "-_" for c in key):
            raise ValueError("invalid Jira issue key")
        response=self.client.get(f"{self.base_url}/rest/api/3/issue/{key}",headers={"Authorization":"Basic "+b64encode(f"{self.email}:{self.token}".encode()).decode(),"Accept":"application/json"},params={"fields":"summary,status,issuetype"})
        if response.status_code!=200: raise RuntimeError(f"Jira returned HTTP {response.status_code}")
        data=response.json()
        try:
            fields=data["fields"]
            return JiraIssue(str(data["key"]),str(fields["summary"]),str(fields["status"]["name"]),str(fields["issuetype"]["name"]))
        except (TypeError,KeyError) as exc: raise ValueError("malformed Jira issue payload") from exc
