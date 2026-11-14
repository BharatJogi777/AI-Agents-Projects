import pytest
from app.risk_register import Risk,generate_register
def test_register_prioritizes_high_risks():
 r=generate_register([Risk("low","Minor",1,2,"team","monitor"),Risk("high","Leak",5,5,"sec","restrict access")])
 assert r[0].risk_id=="high" and r[0].level=="critical"
def test_invalid_risk_rejected():
 with pytest.raises(ValueError): generate_register([Risk("x","Risk",6,2,"team","fix")])
 with pytest.raises(ValueError): generate_register([Risk("x","Risk",2,2,"team","fix"),Risk("x","Dup",2,2,"team","fix")])
