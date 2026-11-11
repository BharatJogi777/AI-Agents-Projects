import pytest
from preference_memory import PreferenceMemory
def test_confirmed_preference_provenance_and_delete():
 m=PreferenceMemory();p=m.remember("u","learning_style","stepwise",True)
 assert p.provenance=="explicit_user_confirmation" and m.get("u")== (p,)
 assert m.forget("u","learning_style")==1 and not m.get("u")
def test_unconfirmed_and_sensitive_rejected():
 m=PreferenceMemory()
 with pytest.raises(PermissionError):m.remember("u","language","English",False)
 with pytest.raises(PermissionError):m.remember("u","health","private",True)
