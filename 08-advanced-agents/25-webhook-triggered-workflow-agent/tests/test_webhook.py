import hashlib, hmac
import pytest
from app.webhook import verify_webhook

def signed(body, secret, ts):
    return hmac.new(secret.encode(), str(ts).encode()+b"."+body, hashlib.sha256).hexdigest()

def test_valid_signature_creates_intent_only():
    body=b'{"id":"evt-1"}'
    result=verify_webhook(body=body,signature=signed(body,"secret",1000),secret="secret",timestamp=1000,now=1000,event_id="evt-1",event_type="invoice.paid")
    assert result.action == "reconcile_invoice"

def test_rejects_bad_signature_stale_and_replay():
    body=b"payload"
    with pytest.raises(ValueError): verify_webhook(body=body,signature="bad",secret="s",timestamp=10,now=10,event_id="x",event_type="ticket.created")
    sig=signed(body,"s",10)
    with pytest.raises(ValueError): verify_webhook(body=body,signature=sig,secret="s",timestamp=10,now=999,event_id="x",event_type="ticket.created")
    with pytest.raises(ValueError): verify_webhook(body=body,signature=sig,secret="s",timestamp=10,now=10,event_id="x",event_type="ticket.created",seen_ids={"x"})

def test_rejects_unknown_event_and_missing_payload():
    with pytest.raises(ValueError): verify_webhook(body=b"x",signature="s",secret="s",timestamp=1,now=1,event_id="x",event_type="unknown")
    with pytest.raises(ValueError): verify_webhook(body=b"",signature="s",secret="s",timestamp=1,now=1,event_id="x",event_type="invoice.paid")
