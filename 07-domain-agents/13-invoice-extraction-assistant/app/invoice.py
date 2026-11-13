"""Extract common invoice fields from OCR text; this is not an OCR engine."""
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass(frozen=True)
class InvoiceFields:
    invoice_number: str|None
    invoice_date: str|None
    currency: str|None
    total: Decimal|None
    missing_fields: tuple[str,...]

def extract_invoice_fields(ocr_text: str) -> InvoiceFields:
    if not isinstance(ocr_text,str) or not ocr_text.strip(): raise ValueError("ocr_text is required")
    def find(pattern):
        m=re.search(pattern,ocr_text,re.I|re.M); return m.group(1).strip() if m else None
    number=find(r"(?:invoice\s*(?:number|no\.?|#))\s*[:#-]?\s*([A-Z0-9][A-Z0-9/-]{1,})")
    date=find(r"(?:invoice\s*date|date)\s*[:#-]?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
    currency=find(r"\b(USD|EUR|GBP|INR)\b")
    raw=find(r"(?:grand\s*total|total\s*due|invoice\s*total|total)\s*[:=]?\s*(?:USD|EUR|GBP|INR|[$€£₹])?\s*([0-9,]+\.\d{2})")
    try: total=Decimal(raw.replace(",","")) if raw else None
    except InvalidOperation: total=None
    values={"invoice_number":number,"invoice_date":date,"currency":currency,"total":total}
    missing=tuple(k for k,v in values.items() if v is None)
    return InvoiceFields(number,date,currency,total,missing)
