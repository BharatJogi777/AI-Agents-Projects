"""Read-only Slack message search boundary with strict result bounds."""
from dataclasses import dataclass
from typing import Protocol

class Response(Protocol):
    status_code:int
    def json(self)->object: ...
class Client(Protocol):
    def get(self,url:str,*,headers:dict[str,str],params:dict[str,str])->Response: ...

@dataclass(frozen=True)
class SlackMessage:
    channel:str
    user:str
    text:str
    timestamp:str

class SlackSearch:
    def __init__(self,client:Client,token:str):
        if not token.startswith("xoxb-") and not token.startswith("xoxp-"):
            raise ValueError("Slack bot or user token required")
        self.client,self.token=client,token

    def search(self,query:str,*,limit:int=10)->list[SlackMessage]:
        if not query.strip() or not 1<=limit<=100: raise ValueError("query and bounded limit required")
        response=self.client.get("https://slack.com/api/search.messages",headers={"Authorization":f"Bearer {self.token}"},params={"query":query,"count":str(limit),"sort":"timestamp"})
        if response.status_code!=200: raise RuntimeError(f"Slack HTTP {response.status_code}")
        data=response.json()
        if not isinstance(data,dict) or data.get("ok") is not True: raise RuntimeError("Slack search failed")
        matches=data.get("messages",{}).get("matches",[])
        if not isinstance(matches,list): raise ValueError("malformed Slack response")
        results=[]
        for item in matches[:limit]:
            try: results.append(SlackMessage(str(item["channel"]["name"]),str(item["user"]),str(item["text"])[:500],str(item["ts"])))
            except (KeyError,TypeError) as exc: raise ValueError("malformed Slack message") from exc
        return results
