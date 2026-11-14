import pytest
from app.business_report import draft_report

def test_report_preserves_metrics_sources_and_caveats():
    report=draft_report(title="Q3 review",metrics=[{"name":"Revenue","value":"$2m","source":"Finance export"}],observations=["Renewals improved"],caveats=["Unaudited figures"])
    assert report.key_findings[0]=="Revenue: $2m (source: Finance export)"
    assert report.source_labels==("Finance export",)
    assert report.caveats==("Unaudited figures",)

def test_empty_evidence_is_explicit():
    report=draft_report(title="Weekly update",metrics=[],observations=[])
    assert "No findings" in report.executive_summary

def test_rejects_metric_without_source():
    with pytest.raises(ValueError,match="source"):
        draft_report(title="Report",metrics=[{"name":"Revenue","value":10}],observations=[])
