"""
Record.
"""
from dataclasses import dataclass
from functools import total_ordering
from typing import Union


@dataclass(frozen=True)
@total_ordering
class Record:
    """
    Record.
    """

    page_no: int
    url: str
    code: Union[str, int]
    request_error: str

    def __lt__(self, other: "Record") -> int:
        if self.page_no != other.page_no:
            return self.page_no < other.page_no
        return self.url < other.url
