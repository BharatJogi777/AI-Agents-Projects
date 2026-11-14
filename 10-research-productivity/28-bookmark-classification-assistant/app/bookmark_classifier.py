"""Classify supplied bookmarks using transparent URL and title heuristics."""
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class BookmarkLabel:
    bookmark_id: str
    category: str
    reason: str

_RULES={"code":("github.com","gitlab.com","stackoverflow.com"),"research":("arxiv.org","scholar.google.com","pubmed.ncbi.nlm.nih.gov"),"news":("news.","reuters.com","bbc.com"),"video":("youtube.com","youtu.be","vimeo.com")}

def classify_bookmarks(*, bookmarks: list[dict[str,str]]) -> tuple[BookmarkLabel,...]:
    if not isinstance(bookmarks,list): raise ValueError("bookmarks must be a list")
    result=[]; seen=set()
    for item in bookmarks:
        if not isinstance(item,dict) or not isinstance(item.get("id"),str) or not item["id"].strip() or not isinstance(item.get("url"),str):
            raise ValueError("each bookmark needs a non-empty id and URL")
        if item["id"] in seen: raise ValueError("bookmark IDs must be unique")
        seen.add(item["id"])
        parsed=urlparse(item["url"])
        if parsed.scheme not in ("http","https") or not parsed.hostname: raise ValueError("bookmark URL must be HTTP(S)")
        host=parsed.hostname.lower(); category="other"; reason="no configured host rule matched"
        for label,hosts in _RULES.items():
            if any(host==h or host.endswith("."+h) or (h.endswith(".") and host.startswith(h)) for h in hosts):
                category,reason=label,"matched configured hostname rule"; break
        result.append(BookmarkLabel(item["id"],category,reason))
    return tuple(result)
