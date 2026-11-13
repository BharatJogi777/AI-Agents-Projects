import pytest

from app import IncrementalJSONDecoder, IncrementalJSONError


def test_fragmented_object():
    decoder = IncrementalJSONDecoder()
    assert decoder.feed('{"name":') == []
    assert decoder.feed('"Ada","n":2}') == [{"name": "Ada", "n": 2}]
    assert decoder.finish() == []


def test_multiple_values_in_one_chunk():
    decoder = IncrementalJSONDecoder()
    assert decoder.feed('{"a":1} [2,3] true null "ok"') == [
        {"a": 1}, [2, 3], True, None, "ok"
    ]


def test_multiple_values_across_chunks():
    decoder = IncrementalJSONDecoder()
    assert decoder.feed('{"a":1} {"b"') == [{"a": 1}]
    assert decoder.feed(':2}') == [{"b": 2}]


def test_incomplete_stream_fails_at_eof():
    decoder = IncrementalJSONDecoder()
    decoder.feed('{"a":')
    with pytest.raises(IncrementalJSONError, match="incomplete or invalid"):
        decoder.finish()


def test_pending_buffer_limit_and_input_type():
    decoder = IncrementalJSONDecoder(max_buffer_chars=5)
    with pytest.raises(IncrementalJSONError, match="exceeds"):
        decoder.feed('"abcdef')
    with pytest.raises(TypeError, match="str"):
        IncrementalJSONDecoder().feed(b"{}")


def test_complete_values_do_not_count_toward_pending_limit():
    decoder = IncrementalJSONDecoder(max_buffer_chars=5)
    values = decoder.feed("{} " * 100)
    assert values == [{}] * 100
    assert decoder.buffered_chars == 0


def test_only_json_whitespace_is_ignored():
    decoder = IncrementalJSONDecoder()
    decoder.feed(" \t\r\n")
    assert decoder.finish() == []
    decoder.reset()
    decoder.feed("\u00a0")
    with pytest.raises(IncrementalJSONError):
        decoder.finish()


def test_non_finite_numbers_are_rejected():
    decoder = IncrementalJSONDecoder()
    decoder.feed("NaN")
    with pytest.raises(IncrementalJSONError):
        decoder.finish()


def test_finish_is_terminal_until_reset():
    decoder = IncrementalJSONDecoder()
    assert decoder.feed("1") == [1]
    assert decoder.finish() == []
    with pytest.raises(IncrementalJSONError, match="already finished"):
        decoder.feed("2")
    decoder.reset()
    assert decoder.feed("2") == [2]
