import pytest
from app.terraform_drift import explain_drift

def test_reports_and_redacts_sensitive_drift():
    result=explain_drift({"db":{"size":10,"password":"old"}},{"db":{"size":20,"password":"new"}})
    assert len(result)==2
    secret=next(x for x in result if x["sensitive"])
    assert secret["desired"] == "[REDACTED]"

def test_added_attribute_is_detected():
    result=explain_drift({},{"region":"ap-south-1"})
    assert result[0]["change"] == "added"
