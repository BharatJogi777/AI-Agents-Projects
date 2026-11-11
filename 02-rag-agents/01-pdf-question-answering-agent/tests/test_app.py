import pytest
from io import BytesIO
from pypdf import PdfWriter
from app import extract_pdf,PDFExtractionError
def test_page_limit_and_empty_pdf():
 w=PdfWriter(); w.add_blank_page(width=72,height=72); w.add_blank_page(width=72,height=72); b=BytesIO(); w.write(b)
 assert extract_pdf(b.getvalue(),1)==[]
def test_invalid_pdf_and_limit():
 with pytest.raises(PDFExtractionError): extract_pdf(b"not pdf")
 with pytest.raises(ValueError): extract_pdf(b"",0)
