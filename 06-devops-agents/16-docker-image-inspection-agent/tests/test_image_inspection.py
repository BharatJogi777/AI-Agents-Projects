import pytest
from app.image_inspection import inspect_image

def test_reports_root_user_and_large_layer():
    result=inspect_image({"name":"api:v1","user":"root","layers":[{"size_bytes":150000000}]})
    codes={x["code"] for x in result["findings"]}
    assert {"ROOT_DEFAULT_USER","LARGE_LAYER","MISSING_DIGEST"} <= codes

def test_rejects_bad_layer_size():
    with pytest.raises(ValueError): inspect_image({"name":"api","layers":[{"size_bytes":-1}]})
