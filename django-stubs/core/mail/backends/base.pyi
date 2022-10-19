from types import TracebackType
from typing import Any, Optional, Sequence, Type, TypeVar

from django.core.mail.message import EmailMessage

_T = TypeVar("_T", bound="BaseEmailBackend")

class BaseEmailBackend:
    fail_silently: bool
    def __init__(self, fail_silently: bool = ..., **kwargs: Any) -> None: ...
    def open(self) -> Optional[bool]: ...
    def close(self) -> None: ...
    def __enter__(self: _T) -> _T: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None: ...
    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int: ...
