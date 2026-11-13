"""Normalize OCR-extracted receipt fields while preserving uncertainty."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Receipt:
    merchant:str
    date:str
    currency:str
    subtotal:float
    tax:float
    total:float
    confidence:float
def validate_receipt(r:Receipt)->dict:
    if not r.merchant.strip() or not r.date.strip() or len(r.currency.strip())!=3: raise ValueError("merchant, date, and three-letter currency are required")
    if min(r.subtotal,r.tax,r.total)<0 or not 0<=r.confidence<=1: raise ValueError("amounts or confidence outside valid range")
    consistent=abs((r.subtotal+r.tax)-r.total)<=0.02
    return {"merchant":r.merchant.strip(),"date":r.date,"currency":r.currency.upper(),"subtotal":r.subtotal,"tax":r.tax,"total":r.total,
            "arithmetic_consistent":consistent,"requires_review":r.confidence<0.85 or not consistent,"ocr_confidence":r.confidence}
