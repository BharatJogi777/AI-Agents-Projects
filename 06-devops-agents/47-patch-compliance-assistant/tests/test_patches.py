from app.patches import assess_patch_compliance
import pytest

def test_flags_outdated_package():
    result=assess_patch_compliance([{"asset":"vm-1","package":"openssl","installed_version":"1.0.0"}],{"openssl":"1.1.0"})
    assert result[0].status=="outdated"

def test_rejects_malformed_version():
    with pytest.raises(ValueError): assess_patch_compliance([{"asset":"vm","package":"openssl","installed_version":"latest"}],{"openssl":"1.2.0"})
