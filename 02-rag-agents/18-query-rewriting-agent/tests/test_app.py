import pytest
from app import rewrite_query
def test_rewrites(): assert rewrite_query("reset token",lambda q:["password reset","reset token"," account recovery "],2)==["reset token","password reset","account recovery"]
def test_validation():
 with pytest.raises(ValueError): rewrite_query("",lambda q:[])
 with pytest.raises(TypeError): rewrite_query("ok",lambda q:None)
