from dataclasses import dataclass,field
from urllib.parse import urlsplit
@dataclass
class NavigationSession:
    allowed_hosts:set[str]
    history:list[str]=field(default_factory=list)
    current:str|None=None
    def navigate(self,url:str)->str:
        p=urlsplit(url)
        if p.scheme!="https" or p.hostname not in self.allowed_hosts: raise ValueError("navigation target is not allowlisted HTTPS")
        if self.current: self.history.append(self.current)
        self.current=url
        return self.current
    def back(self)->str:
        if not self.history: raise LookupError("no previous navigation state")
        self.current=self.history.pop()
        return self.current
    def snapshot(self)->dict:
        return {"current":self.current,"history":list(self.history),"can_go_back":bool(self.history)}
