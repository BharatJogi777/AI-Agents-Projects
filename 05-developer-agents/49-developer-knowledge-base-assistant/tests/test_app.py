import pytest
from app.knowledge_base import Article, search_knowledge

def test_search_returns_ranked_sources():
    docs=[Article("Deploy service","deploy with helm","runbook/deploy"),Article("Database","postgres backups","db/backup")]
    result=search_knowledge("deploy service",docs)
    assert result[0]["source"] == "runbook/deploy"

def test_empty_query_and_bad_limit_rejected():
    with pytest.raises(ValueError): search_knowledge(" ",[])
    with pytest.raises(ValueError): search_knowledge("x",[],limit=0)
