from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
@dataclass(frozen=True)
class Block:
 index:int; kind:str; text:str
def extract_docx(source:str|Path|bytes)->list[Block]:
 from docx import Document
 from docx.text.paragraph import Paragraph
 from docx.table import Table
 doc=Document(BytesIO(source) if isinstance(source,bytes) else str(source)); blocks=[]
 for child in doc.element.body.iterchildren():
  tag=child.tag.rsplit("}",1)[-1]
  if tag=="p":
   text=Paragraph(child,doc).text.strip()
   if text: blocks.append(Block(len(blocks)+1,"paragraph",text))
  elif tag=="tbl":
   for row in Table(child,doc).rows:
    text=" | ".join(v for v in (c.text.strip().replace("\\n"," ") for c in row.cells) if v)
    if text: blocks.append(Block(len(blocks)+1,"table_row",text))
 return blocks
