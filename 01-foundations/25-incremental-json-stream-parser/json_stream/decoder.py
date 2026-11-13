"""Incremental parser for concatenated JSON values in text streams."""
from __future__ import annotations

import json
from typing import Any

from .contracts import IncrementalJSONError


def _reject_non_finite(value: str) -> None:
    raise ValueError(f"non-standard JSON numeric constant: {value}")


class IncrementalJSONDecoder:
    """Decode one or more concatenated JSON values across arbitrary text chunks.

    Values are emitted as soon as they are complete. An incomplete suffix is
    retained until the next call to :meth:`feed`. Call :meth:`finish` at EOF
    to distinguish a clean end from a truncated or malformed value.
    """

    def __init__(self, max_buffer_chars: int = 1_000_000) -> None:
        if type(max_buffer_chars) is not int or max_buffer_chars < 2:
            raise ValueError("max_buffer_chars must be an integer >= 2")
        self.max_buffer_chars = max_buffer_chars
        self._decoder = json.JSONDecoder(parse_constant=_reject_non_finite)
        self._buffer = ""
        self._finished = False

    @property
    def buffered_chars(self) -> int:
        """Number of characters currently retained for an incomplete value."""
        return len(self._buffer)

    def feed(self, chunk: str) -> list[Any]:
        """Consume a text chunk and return every complete JSON value in it."""
        if self._finished:
            raise IncrementalJSONError("decoder is already finished; call reset()")
        if not isinstance(chunk, str):
            raise TypeError("chunk must be str")
        self._buffer += chunk
        values: list[Any] = []

        while True:
            # JSON permits only the four JSON whitespace characters. lstrip()
            # would also discard Unicode whitespace that is invalid in JSON.
            offset = 0
            while offset < len(self._buffer) and self._buffer[offset] in " \t\r\n":
                offset += 1
            if offset == len(self._buffer):
                self._buffer = ""
                break

            candidate = self._buffer[offset:]
            try:
                value, end = self._decoder.raw_decode(candidate)
            except (json.JSONDecodeError, ValueError):
                # raw_decode cannot tell whether a prefix is truncated or
                # malformed. Retain it and let later input or finish() decide.
                self._buffer = candidate
                break

            values.append(value)
            self._buffer = candidate[end:]

        if len(self._buffer) > self.max_buffer_chars:
            self._buffer = ""
            raise IncrementalJSONError(
                f"incomplete JSON value exceeds max_buffer_chars={self.max_buffer_chars}"
            )
        return values

    def finish(self) -> list[Any]:
        """Mark EOF and emit a final value, or raise for incomplete input."""
        if self._finished:
            return []
        self._finished = True
        candidate = self._buffer
        offset = 0
        while offset < len(candidate) and candidate[offset] in " \t\r\n":
            offset += 1
        candidate = candidate[offset:]
        if not candidate:
            self._buffer = ""
            return []
        try:
            value, end = self._decoder.raw_decode(candidate)
        except (json.JSONDecodeError, ValueError) as exc:
            self._buffer = ""
            raise IncrementalJSONError("stream ended with incomplete or invalid JSON") from exc
        if candidate[end:].strip(" \t\r\n"):
            self._buffer = ""
            raise IncrementalJSONError("trailing non-JSON data after final value")
        self._buffer = ""
        return [value]

    def reset(self) -> None:
        """Reuse this decoder for a new independent stream."""
        self._buffer = ""
        self._finished = False
