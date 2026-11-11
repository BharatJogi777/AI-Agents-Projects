from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
@dataclass(frozen=True)
class SheetRow: sheet:str; row_number:int; values:tuple[object,...]
def extract_workbook(source:str|Path|bytes,max_bytes:int=20000000,max_rows:int=100000)->list[SheetRow]:
 from openpyxl import load_workbook
 if isinstance(source,bytes):
  if len(source)>max_bytes: raise ValueError("workbook too large")
  stream=BytesIO(source)
 else:
  if Path(source).stat().st_size>max_bytes: raise ValueError("workbook too large")
  stream=source
 wb=load_workbook(stream,read_only=True,data_only=True); rows=[]
 try:
  for ws in wb.worksheets:
   for number,values in enumerate(ws.iter_rows(values_only=True),1):
    if number>max_rows: raise ValueError(f"sheet {ws.title} exceeds row limit")
    vals=tuple(v.isoformat() if hasattr(v,"isoformat") else v for v in values)
    if any(v is not None for v in vals): rows.append(SheetRow(ws.title,number,vals))
 finally: wb.close()
 return rows
