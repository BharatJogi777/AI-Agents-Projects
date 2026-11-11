import csv,io
from dataclasses import dataclass
@dataclass(frozen=True)
class CSVRecord: row_number:int; values:dict[str,str]
def parse_csv(source:str|bytes,max_bytes:int=5000000,max_rows:int=100000)->list[CSVRecord]:
 if isinstance(source,bytes):
  if len(source)>max_bytes: raise ValueError("CSV too large")
  source=source.decode("utf-8-sig")
 elif isinstance(source,str):
  if len(source.encode())>max_bytes: raise ValueError("CSV too large")
 else: raise TypeError("source must be str or bytes")
 reader=csv.DictReader(io.StringIO(source,newline=""))
 if not reader.fieldnames or any(not h or not h.strip() for h in reader.fieldnames): raise ValueError("CSV requires non-empty headers")
 if len(set(reader.fieldnames))!=len(reader.fieldnames): raise ValueError("duplicate headers")
 rows=[]
 for number,row in enumerate(reader,2):
  if number-1>max_rows: raise ValueError("too many rows")
  rows.append(CSVRecord(number,{k:(v or "") for k,v in row.items()}))
 return rows
