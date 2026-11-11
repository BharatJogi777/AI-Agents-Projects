import pytest
from app import *
def test_lifecycle():
 m=RunManager(); r=m.create(); m.start(r.id); end=m.finish(r.id,Status.SUCCEEDED)
 assert end.finished_at>=end.started_at
def test_isolation_and_guards():
 m=RunManager(); a=m.create(); b=m.create(); m.start(a.id)
 assert m.get(b.id).status is Status.CREATED
 with pytest.raises(InvalidLifecycle): m.finish(b.id,Status.SUCCEEDED)
 with pytest.raises(KeyError): m.get("missing")
