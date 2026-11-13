import pytest
from app.impact import analyze_impact

def test_finds_transitive_dependents():
 r=analyze_impact({'db':[],'api':['db'],'worker':['api']},'db')
 assert r.affected_components==('api','worker')

def test_rejects_unknown_edge():
 with pytest.raises(ValueError): analyze_impact({'api':['missing']},'api')
