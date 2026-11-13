from app.pii_masking import detect_and_mask_pii

def test_masks_email_phone_and_valid_ipv4():
    result = detect_and_mask_pii(text="a@example.com +1 415 555 0123 192.168.1.1")
    assert result["count"] == 3 and "a@example.com" not in result["masked_text"]

def test_ignores_invalid_ipv4():
    result = detect_and_mask_pii(text="999.999.999.999")
    assert result["count"] == 0
