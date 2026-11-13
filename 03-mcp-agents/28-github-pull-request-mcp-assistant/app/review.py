"""Produce bounded, read-only pull request review context."""
from dataclasses import dataclass
from typing import Protocol

class Client(Protocol):
    def get(self,url:str,*,headers:dict[str,str])->object: ...

@dataclass(frozen=True)
class PullRequestContext:
    number:int
    title:str
    state:str
    url:str

class PullRequestReader:
    def __init__(self,client:Client,token:str):
        if not token.strip(): raise ValueError("token required")
        self.client,self.token=client,token

    def get(self,owner:str,repo:str,number:int)->PullRequestContext:
        if not owner or not repo or number<1: raise ValueError("invalid pull request reference")
        response=self.client.get(f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}",headers={"Authorization":f"Bearer {self.token}","Accept":"application/vnd.github+json"})
        status=getattr(response,"status_code",None)
        if status!=200: raise RuntimeError(f"GitHub API returned HTTP {status}")
        data=response.json()
        if not isinstance(data,dict): raise ValueError("unexpected pull request payload")
        try:
            return PullRequestContext(int(data["number"]),str(data["title"]),str(data["state"]),str(data["html_url"]))
        except (KeyError,TypeError,ValueError) as exc: raise ValueError("malformed pull request payload") from exc
