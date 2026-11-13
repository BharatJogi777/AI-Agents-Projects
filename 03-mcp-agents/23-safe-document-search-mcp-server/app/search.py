"""Search only indexed documents visible to the requesting principal."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Document:
    document_id: str
    title: str
    text: str
    allowed_principals: frozenset[str]

class DocumentSearch:
    def __init__(self, documents: list[Document], *, max_results: int=20):
        if max_results < 1:
            raise ValueError("max_results must be positive")
        ids=[d.document_id for d in documents]
        if len(ids)!=len(set(ids)):
            raise ValueError("document IDs must be unique")
        self._documents=tuple(documents)
        self.max_results=max_results

    def search(self, query: str, *, principal: str, limit: int=10)->list[dict[str,str]]:
        terms={term.casefold() for term in query.split() if term.strip()}
        if not terms or not principal.strip():
            raise ValueError("query and principal are required")
        if not 1<=limit<=self.max_results:
            raise ValueError("limit outside allowed range")
        matches=[]
        for doc in self._documents:
            if principal not in doc.allowed_principals:
                continue
            haystack=f"{doc.title} {doc.text}".casefold()
            score=sum(haystack.count(term) for term in terms)
            if score:
                matches.append((score,doc))
        matches.sort(key=lambda pair:(-pair[0],pair[1].document_id))
        return [{"document_id":d.document_id,"title":d.title,"snippet":d.text[:240]} for _,d in matches[:limit]]
