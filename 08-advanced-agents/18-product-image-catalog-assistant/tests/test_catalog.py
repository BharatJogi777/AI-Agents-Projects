import pytest
from app.catalog import ProductImage,create_catalog_entry
def test_creates_unpublished_entry():
 r=create_catalog_entry(ProductImage("img-1","SKU1","Blue shirt","apparel",("Blue","Casual","blue")),set())
 assert r["tags"]==["blue","casual"] and not r["published"]
def test_rejects_duplicate_sku():
 with pytest.raises(ValueError): create_catalog_entry(ProductImage("i","S","T","C",()),{"S"})
def test_rejects_missing_title():
 with pytest.raises(ValueError): create_catalog_entry(ProductImage("i","S"," ","C",()),set())
