import pytest
from app.queue import SQLiteJobQueue

def test_enqueue_claim_complete(tmp_path):
    q=SQLiteJobQueue(str(tmp_path/"q.db")); q.enqueue("j1",{"x":1})
    job=q.claim(); assert job.payload=={"x":1} and job.attempts==1
    q.complete("j1",{"ok":True}); assert q.claim() is None; q.close()

def test_retry_requeues_job(tmp_path):
    q=SQLiteJobQueue(str(tmp_path/"q.db")); q.enqueue("j",{})
    q.claim(); q.retry("j"); assert q.claim().attempts==2; q.close()

def test_duplicate_job_id_rejected(tmp_path):
    q=SQLiteJobQueue(str(tmp_path/"q.db")); q.enqueue("j",{})
    with pytest.raises(Exception): q.enqueue("j",{})
    q.close()
