import urllib
import urllib.parse
from base64 import b64decode, b64encode
from collections.abc import Sequence
from typing import NamedTuple


class Cursor(NamedTuple):
    offset: int
    reverse: bool
    position: str | None

    @classmethod
    def decode(cls, encoded: str) -> 'Cursor':
        try:
            qs = b64decode(encoded.encode('ascii')).decode('ascii')
            tokens = urllib.parse.parse_qs(qs, keep_blank_values=True)

            offset = int(tokens.get('o', ['0'])[0])
            reverse = bool(int(tokens.get('r', ['0'])[0]))
            position = tokens.get('p', [None])[0]
        except (TypeError, ValueError) as exc:
            msg = 'Invalid cursor format'
            raise ValueError(msg) from exc
        else:
            return cls(offset=offset, reverse=reverse, position=position)

    def encode(self) -> str:
        tokens = {}
        if self.offset != 0:
            tokens['o'] = str(self.offset)
        if self.reverse:
            tokens['r'] = '1'
        if self.position is not None:
            tokens['p'] = self.position
        qs = urllib.parse.urlencode(tokens, doseq=True)

        return b64encode(qs.encode('ascii')).decode('ascii')


class Paginator[T: object](NamedTuple):
    results: Sequence[T]
    next: str | None
    previous: str | None
