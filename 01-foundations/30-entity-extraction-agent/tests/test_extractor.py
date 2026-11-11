import pytest
from app import EntityExtractor,EntityExtractionError
def test_extracts_grounded_entity_with_offsets():
    e=EntityExtractor(lambda _: [{"kind":"person","value":"Ada","evidence":"Ada Lovelace"}],{"person"})
    result=e.extract("Met Ada Lovelace yesterday.")
    assert result[0].start==4 and result[0].end==16
def test_rejects_ungrounded_or_unknown_entities():
    e=EntityExtractor(lambda _: [{"kind":"person","value":"Grace","evidence":"Grace Hopper"}],{"person"})
    with pytest.raises(EntityExtractionError): e.extract("Met Ada.")
    e=EntityExtractor(lambda _: [{"kind":"animal","value":"cat","evidence":"cat"}],{"person"})
    with pytest.raises(EntityExtractionError): e.extract("cat")
def test_deduplicates_and_checks_input_size():
    e=EntityExtractor(lambda _: [{"kind":"org","value":"ACME","evidence":"ACME"},{"kind":"org","value":"ACME","evidence":"ACME"}],{"org"},10)
    assert len(e.extract("ACME"))==1
    with pytest.raises(EntityExtractionError): e.extract("x"*11)
def test_empty_and_wrong_model_output():
    with pytest.raises(ValueError): EntityExtractor(lambda _:[],{"person"}).extract(" ")
    with pytest.raises(EntityExtractionError): EntityExtractor(lambda _:None,{"person"}).extract("text")
