import pytest
from app import *
def test_consent_isolation():
 m=PreferenceMemory();m.remember("u1","learning_style","stepwise",True)
 assert len(m.get("u1"))==1 and not m.get("u2")
def test_reject_unconfirmed_sensitive():
 m=PreferenceMemory()
 with pytest.raises(PermissionError):m.remember("u","language","English",False)
 with pytest.raises(PermissionError):m.remember("u","health","private",True)
def test_forget():
 m=PreferenceMemory();m.remember("u","format","bullets",True);assert m.forget("u")==1
