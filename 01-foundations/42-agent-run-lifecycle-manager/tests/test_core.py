from datetime import datetime,timezone,timedelta
import pytest
from agent_run_manager import *
def test_lifecycle_and_utc_timestamps():
 now=[datetime(2026,1,1,tzinfo=timezone.utc)];m=RunManager(clock=lambda:now[0]);r=m.create("a")
 now[0]+=timedelta(seconds=2);s=m.start("a");now[0]+=timedelta(seconds=3);d=m.finish("a",Status.SUCCEEDED)
 assert r.status is Status.CREATED and d.finished_at-s.started_at==timedelta(seconds=3)
def test_capacity_and_unique_ids():
 m=RunManager(1);m.create("a")
 with pytest.raises(ValueError):m.create("a")
 with pytest.raises(RuntimeError):m.create("b")
def test_only_terminal_runs_can_be_deleted():
 m=RunManager();r=m.create()
 with pytest.raises(InvalidLifecycle):m.delete(r.id)
 m.start(r.id);m.finish(r.id,Status.FAILED,"safe");m.delete(r.id)
 with pytest.raises(RunNotFound):m.get(r.id)
def test_invalid_completion():
 m=RunManager();r=m.create()
 with pytest.raises(InvalidLifecycle):m.finish(r.id,Status.SUCCEEDED)
