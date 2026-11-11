import pytest
from app import MetadataFilter,validate_filters,matches
def test_filter():
 f=validate_filters([MetadataFilter("team","eq","payments"),MetadataFilter("age","gte",2)],{"team","age"}); assert matches({"team":"payments","age":3},f) and not matches({"team":"other","age":3},f)
def test_reject_unsafe():
 with pytest.raises(ValueError): validate_filters([MetadataFilter("__class__","eq","x")],{"team"})
 with pytest.raises(ValueError): validate_filters([MetadataFilter("age","gte","2")],{"age"})
