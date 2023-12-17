import pytest
from cheek.cli import field_info_to_click_type
from pydantic.fields import FieldInfo


def test_int():
    f = FieldInfo(annotation=int)
    assert field_info_to_click_type(f) is int


def test_none():
    with pytest.raises(AssertionError):
        field_info_to_click_type(FieldInfo(annotation=None))


def test_union_type():
    f = FieldInfo(annotation=str | None)
    assert field_info_to_click_type(f) is str


