from io import StringIO
from cli_agent import run_cli
def invoke(args,agent):
 out,err=StringIO(),StringIO();code=run_cli(args,agent,out,err);return code,out.getvalue(),err.getvalue()
def test_success_and_injected_agent():
 code,out,err=invoke(["hello"],lambda p:p.upper())
 assert (code,out,err)==(0,"HELLO\n","")
def test_oversized_prompt_has_deterministic_exit_code():
 code,out,err=invoke(["long","--max-chars","2"],lambda p:"unused")
 assert code==2 and out=="" and "limit" in err
def test_exception_is_sanitized():
 code,out,err=invoke(["task"],lambda p:(_ for _ in ()).throw(RuntimeError("secret token")))
 assert code==1 and "RuntimeError" in err and "secret" not in err
def test_non_string_result_is_rejected():
 code,out,err=invoke(["task"],lambda p:{"answer":1})
 assert code==1 and "invalid response" in err
