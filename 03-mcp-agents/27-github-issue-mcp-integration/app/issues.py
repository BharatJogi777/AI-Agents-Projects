"""Minimal GitHub issue client using an injected HTTP transport."""
from dataclasses import dataclass
from typing import Protocol

class Response(Protocol):
    status_code:int
    def json(self)->object: ...
class HttpClient(Protocol):
    def get(self,url:str,*,headers:dict[str,str],params:dict[str,str])->Response: ...

@dataclass(frozen=True)
class Issue:
    number:int
    title:str
    state:str
    html_url:str

class GitHubIssues:
    def __init__(self,client:HttpClient,token:str):
        if not token.strip(): raise ValueError("GitHub token is required")
        self.client,self._token=client,token

    def list_issues(self,owner:str,repo:str,*,state:str="open",limit:int=20)->list[Issue]:
        if not owner or not repo or state not in {"open","closed","all"} or not 1<=limit<=100:
            raise ValueError("invalid repository, state, or limit")
        response=self.client.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers={"Authorization":f"Bearer {self._token}","Accept":"application/vnd.github+json"},
            params={"state":state,"per_page":str(limit)})
        if response.status_code!=200: raise RuntimeError(f"GitHub API returned HTTP {response.status_code}")
        payload=response.json()
        if not isinstance(payload,list): raise ValueError("unexpected GitHub response")
        issues=[]
        for item in payload:
            if not isinstance(item,dict) or "pull_request" in item: continue
            try: issues.append(Issue(int(item["number"]),str(item["title"]),str(item["state"]),str(item["html_url"])))
            except (KeyError,TypeError,ValueError) as exc: raise ValueError("malformed issue item") from exc
        return issues
