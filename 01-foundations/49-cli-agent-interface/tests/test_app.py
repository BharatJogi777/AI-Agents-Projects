from app import run_cli
def test_success(capsys):
 calls=[]; assert run_cli(["hello"],lambda p:calls.append(p) or "done")==0
 assert calls==["hello"] and capsys.readouterr().out.strip()=="done"
def test_validation_and_errors(capsys):
 assert run_cli(["12345","--max-chars","4"],lambda p:"x")==2
 assert run_cli(["hi"],lambda p:1/0)==1
 out=capsys.readouterr().out; assert "oversized" in out and "ZeroDivisionError" in out
