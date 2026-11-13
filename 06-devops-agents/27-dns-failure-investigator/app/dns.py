"""Analyze DNS observations supplied by a resolver or diagnostic capture."""
from dataclasses import dataclass

@dataclass(frozen=True)
class DNSFinding:
    hostname: str
    severity: str
    issue: str
    next_check: str

NEXT={
 "NXDOMAIN":"Verify the record name, hosted zone, delegation, and recent record changes.",
 "SERVFAIL":"Inspect authoritative nameservers, DNSSEC validation, and upstream resolver health.",
 "TIMEOUT":"Check network reachability to resolvers, UDP/TCP 53 rules, and resolver availability.",
 "REFUSED":"Check resolver ACLs, recursion policy, and query source authorization.",
}

def investigate_dns(observations: list[dict]) -> list[DNSFinding]:
    if not isinstance(observations,list): raise TypeError("observations must be a list")
    results=[]
    for i,item in enumerate(observations):
        if not isinstance(item,dict): raise ValueError(f"observation {i} must be an object")
        host=item.get("hostname"); status=item.get("status")
        if not isinstance(host,str) or not host.strip(): raise ValueError(f"observation {i} requires hostname")
        if status not in {"NOERROR","NXDOMAIN","SERVFAIL","TIMEOUT","REFUSED"}: raise ValueError(f"{host}: unsupported DNS status")
        if status=="NOERROR":
            answers=item.get("answers",[])
            if not isinstance(answers,list): raise ValueError("answers must be a list")
            if len(set(map(str,answers)))>1: results.append(DNSFinding(host,"medium","Inconsistent answers across observations","Compare resolver cache, TTL, geographic routing, and authoritative responses."))
        else:
            results.append(DNSFinding(host,"high" if status in {"SERVFAIL","TIMEOUT"} else "medium",status,NEXT[status]))
    return results
