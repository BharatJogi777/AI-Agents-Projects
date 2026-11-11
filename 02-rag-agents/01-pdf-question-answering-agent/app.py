from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import BinaryIO
@dataclass(frozen=True)
class Page:
 page_number:int
 text:str
class PDFExtractionError(ValueError): pass
def extract_pdf(source: str|Path|bytes|BinaryIO, max_pages:int=500)->list[Page]:
 if max_pages<1: raise ValueError("max_pages must be positive")
 try:
  from pypdf import PdfReader
  reader=PdfReader(str(source)) if isinstance(source,(str,Path)) else PdfReader(BytesIO(source)) if isinstance(source,bytes) else PdfReader(source)
  if reader.is_encrypted:
   try: reader.decrypt("")
   except Exception as exc: raise PDFExtractionError("encrypted PDF is not supported") from exc
  return [Page(i,(page.extract_text() or "").strip()) for i,page in enumerate(reader.pages[:max_pages],1) if (page.extract_text() or "").strip()]
 except PDFExtractionError: raise
 except Exception as exc: raise PDFExtractionError("could not parse PDF") from exc
