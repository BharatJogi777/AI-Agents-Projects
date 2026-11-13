from app.invoice import extract_invoice_fields
import pytest

def test_extracts_common_invoice_fields():
    result=extract_invoice_fields("Invoice Number: INV-2026-12\nInvoice Date: 2026-11-01\nCurrency: INR\nGrand Total: ₹1,250.00")
    assert result.invoice_number=="INV-2026-12" and str(result.total)=="1250.00" and not result.missing_fields

def test_marks_missing_fields():
    result=extract_invoice_fields("Supplier copy")
    assert "invoice_number" in result.missing_fields and result.total is None
