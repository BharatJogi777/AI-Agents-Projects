import pytest
from app.spreadsheet import validate_sheet, preview_replace, csv_safe_cell

def test_preview_is_non_mutating():
    sheet=validate_sheet(["name"],[["Ada"],["Adam"]])
    result=preview_replace(sheet,column="name",old="Ada",new="Grace")
    assert [x.new_value for x in result]==["Grace","Grace"]
    assert sheet.rows[0][0]=="Ada"

def test_validation_and_formula_safety():
    with pytest.raises(ValueError):
        validate_sheet(["x","x"],[])
    assert csv_safe_cell("=1+1")=="'=1+1"
