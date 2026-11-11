import sqlite3
from dataclasses import dataclass
@dataclass(frozen=True)
class QueryResult: columns:tuple[str,...]; rows:tuple[tuple[object,...],...]; truncated:bool
def execute_readonly(connection:sqlite3.Connection,sql:str,allowed_tables:set[str],max_rows:int=100,max_vm_steps:int=100000)->QueryResult:
 if not sql.strip() or max_rows<1 or max_vm_steps<100: raise ValueError("query and positive execution limits required")
 first=sql.lstrip().split(None,1)[0].casefold()
 if first not in {"select","with"}: raise ValueError("only SELECT queries are allowed")
 allowed={x.casefold() for x in allowed_tables}
 if not allowed: raise ValueError("at least one table must be allowlisted")
 denied={sqlite3.SQLITE_INSERT,sqlite3.SQLITE_UPDATE,sqlite3.SQLITE_DELETE,sqlite3.SQLITE_CREATE_INDEX,sqlite3.SQLITE_CREATE_TABLE,sqlite3.SQLITE_CREATE_TEMP_INDEX,sqlite3.SQLITE_CREATE_TEMP_TABLE,sqlite3.SQLITE_CREATE_TEMP_TRIGGER,sqlite3.SQLITE_CREATE_TEMP_VIEW,sqlite3.SQLITE_CREATE_TRIGGER,sqlite3.SQLITE_CREATE_VIEW,sqlite3.SQLITE_DROP_INDEX,sqlite3.SQLITE_DROP_TABLE,sqlite3.SQLITE_DROP_TEMP_INDEX,sqlite3.SQLITE_DROP_TEMP_TABLE,sqlite3.SQLITE_DROP_TEMP_TRIGGER,sqlite3.SQLITE_DROP_TEMP_VIEW,sqlite3.SQLITE_DROP_TRIGGER,sqlite3.SQLITE_DROP_VIEW,sqlite3.SQLITE_ALTER_TABLE,sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH,sqlite3.SQLITE_PRAGMA}
 steps=0
 def authorize(action,arg1,arg2,db,trigger):
  if action in denied: return sqlite3.SQLITE_DENY
  if action==sqlite3.SQLITE_READ and arg1.casefold() not in allowed and arg1.casefold() not in {"sqlite_master","sqlite_schema"}: return sqlite3.SQLITE_DENY
  if action==sqlite3.SQLITE_FUNCTION and (arg2 or arg1 or "").casefold() in {"load_extension","writefile"}: return sqlite3.SQLITE_DENY
  return sqlite3.SQLITE_OK
 def progress():
  nonlocal steps
  steps+=1000
  return 1 if steps>max_vm_steps else 0
 old_authorizer=None
 try:
  connection.set_authorizer(authorize); connection.set_progress_handler(progress,1000)
  cursor=connection.execute(sql); columns=tuple(x[0] for x in (cursor.description or ())); rows=cursor.fetchmany(max_rows+1)
  return QueryResult(columns,tuple(tuple(x) for x in rows[:max_rows]),len(rows)>max_rows)
 finally:
  connection.set_authorizer(None); connection.set_progress_handler(None,0)
