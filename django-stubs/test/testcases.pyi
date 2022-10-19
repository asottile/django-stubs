import threading
import unittest
from datetime import date
from types import TracebackType
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    overload,
)

from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import ThreadedWSGIServer, WSGIRequestHandler
from django.db import connections as connections  # noqa: F401
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.base import Model
from django.db.models.query import QuerySet, RawQuerySet
from django.forms import BaseFormSet, Form
from django.forms.fields import EmailField
from django.http.response import FileResponse, HttpResponseBase
from django.template.base import Template
from django.test.client import AsyncClient, Client
from django.test.html import Element
from django.test.utils import CaptureQueriesContext, ContextList
from django.utils.functional import classproperty

def to_list(value: Any) -> list[Any]: ...
def assert_and_parse_html(self: Any, html: str, user_msg: str, msg: str) -> Element: ...

class _AssertNumQueriesContext(CaptureQueriesContext):
    test_case: SimpleTestCase = ...
    num: int = ...
    def __init__(self, test_case: Any, num: Any, connection: BaseDatabaseWrapper) -> None: ...

class _AssertTemplateUsedContext:
    test_case: SimpleTestCase = ...
    template_name: str = ...
    rendered_templates: List[Template] = ...
    rendered_template_names: List[str] = ...
    context: ContextList = ...
    def __init__(self, test_case: Any, template_name: Any) -> None: ...
    def on_template_render(self, sender: Any, signal: Any, template: Any, context: Any, **kwargs: Any) -> None: ...
    def test(self) -> None: ...
    def message(self) -> str: ...
    def __enter__(self) -> _AssertTemplateUsedContext: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None: ...

class _AssertTemplateNotUsedContext(_AssertTemplateUsedContext): ...

class _DatabaseFailure:
    wrapped: Any = ...
    message: str = ...
    def __init__(self, wrapped: Any, message: str) -> None: ...
    def __call__(self) -> None: ...

class SimpleTestCase(unittest.TestCase):
    client_class: Type[Client] = ...
    client: Client
    async_client_class: Type[AsyncClient] = ...
    async_client: AsyncClient
    allow_database_queries: bool = ...
    # TODO: str -> Literal['__all__']
    databases: Union[Set[str], str] = ...
    def __call__(self, result: Optional[unittest.TestResult] = ...) -> None: ...
    def settings(self, **kwargs: Any) -> Any: ...
    def modify_settings(self, **kwargs: Any) -> Any: ...
    def assertRedirects(
        self,
        response: HttpResponseBase,
        expected_url: str,
        status_code: int = ...,
        target_status_code: int = ...,
        msg_prefix: str = ...,
        fetch_redirect_response: bool = ...,
    ) -> None: ...
    def assertURLEqual(
        self,
        url1: str | Any,  # Any for reverse_lazy() support
        url2: str | Any,
        msg_prefix: str = ...,
    ) -> None: ...
    def assertContains(
        self,
        response: HttpResponseBase,
        text: Union[bytes, int, str],
        count: Optional[int] = ...,
        status_code: int = ...,
        msg_prefix: str = ...,
        html: bool = ...,
    ) -> None: ...
    def assertNotContains(
        self,
        response: HttpResponseBase,
        text: Union[bytes, str],
        status_code: int = ...,
        msg_prefix: str = ...,
        html: bool = ...,
    ) -> None: ...
    @overload
    def assertFormError(
        self,
        form: Form,
        field: Optional[str],
        errors: Union[List[str], str],
        msg_prefix: str = ...,
    ) -> None: ...
    @overload
    def assertFormError(
        self,
        response: HttpResponseBase,
        form: str,
        field: Optional[str],
        errors: Union[List[str], str],
        msg_prefix: str = ...,
    ) -> None: ...
    @overload
    def assertFormsetError(
        self,
        formset: BaseFormSet,
        form_index: Optional[int],
        field: Optional[str],
        errors: Union[List[str], str],
        msg_prefix: str = ...,
    ) -> None: ...
    @overload
    def assertFormsetError(
        self,
        response: HttpResponseBase,
        formset: str,
        form_index: Optional[int],
        field: Optional[str],
        errors: Union[List[str], str],
        msg_prefix: str = ...,
    ) -> None: ...
    def assertTemplateUsed(
        self,
        response: Optional[Union[HttpResponseBase, str]] = ...,
        template_name: Optional[str] = ...,
        msg_prefix: str = ...,
        count: Optional[int] = ...,
    ) -> Optional[_AssertTemplateUsedContext]: ...
    def assertTemplateNotUsed(
        self, response: Union[HttpResponseBase, str] = ..., template_name: Optional[str] = ..., msg_prefix: str = ...
    ) -> Optional[_AssertTemplateNotUsedContext]: ...
    def assertRaisesMessage(
        self, expected_exception: Type[Exception], expected_message: str, *args: Any, **kwargs: Any
    ) -> Any: ...
    def assertWarnsMessage(
        self, expected_warning: Type[Exception], expected_message: str, *args: Any, **kwargs: Any
    ) -> Any: ...
    def assertFieldOutput(
        self,
        fieldclass: Type[EmailField],
        valid: Dict[str, str],
        invalid: Dict[str, List[str]],
        field_args: Optional[Iterable[Any]] = ...,
        field_kwargs: Optional[Mapping[str, Any]] = ...,
        empty_value: str = ...,
    ) -> Any: ...
    def assertHTMLEqual(self, html1: str, html2: str, msg: Optional[str] = ...) -> None: ...
    def assertHTMLNotEqual(self, html1: str, html2: str, msg: Optional[str] = ...) -> None: ...
    def assertInHTML(self, needle: str, haystack: str, count: Optional[int] = ..., msg_prefix: str = ...) -> None: ...
    def assertJSONEqual(
        self,
        raw: str,
        expected_data: Union[Dict[str, Any], List[Any], str, int, float, bool, None],
        msg: Optional[str] = ...,
    ) -> None: ...
    def assertJSONNotEqual(
        self,
        raw: str,
        expected_data: Union[Dict[str, Any], List[Any], str, int, float, bool, None],
        msg: Optional[str] = ...,
    ) -> None: ...
    def assertXMLEqual(self, xml1: str, xml2: str, msg: Optional[str] = ...) -> None: ...
    def assertXMLNotEqual(self, xml1: str, xml2: str, msg: Optional[str] = ...) -> None: ...

class TransactionTestCase(SimpleTestCase):
    reset_sequences: bool = ...
    available_apps: Any = ...
    fixtures: Any = ...
    multi_db: bool = ...
    serialized_rollback: bool = ...
    def assertQuerysetEqual(
        self,
        qs: Union[Iterator[Any], List[Model], QuerySet, RawQuerySet],
        values: Union[List[None], List[Tuple[str, str]], List[date], List[int], List[str], Set[str], QuerySet],
        transform: Union[Callable, Type[str]] = ...,
        ordered: bool = ...,
        msg: Optional[str] = ...,
    ) -> None: ...
    @overload
    def assertNumQueries(self, num: int, using: str = ...) -> _AssertNumQueriesContext: ...  # type: ignore
    @overload
    def assertNumQueries(
        self, num: int, func: Callable[..., Any], *args: Any, using: str = ..., **kwargs: Any
    ) -> None: ...

class TestCase(TransactionTestCase):
    @classmethod
    def setUpTestData(cls) -> None: ...
    def captureOnCommitCallbacks(cls, *, using: Optional[str] = ..., execute: bool = ...): ...

class CheckCondition:
    conditions: Sequence[Tuple[Callable, str]] = ...
    def __init__(self, *conditions: Tuple[Callable, str]) -> None: ...
    def add_condition(self, condition: Callable, reason: str) -> CheckCondition: ...
    def __get__(self, instance: None, cls: Optional[Type[TransactionTestCase]] = ...) -> bool: ...

def skipIfDBFeature(*features: Any) -> Callable: ...
def skipUnlessDBFeature(*features: Any) -> Callable: ...
def skipUnlessAnyDBFeature(*features: Any) -> Callable: ...

class QuietWSGIRequestHandler(WSGIRequestHandler): ...

class FSFilesHandler(WSGIHandler):
    application: Any = ...
    base_url: Any = ...
    def __init__(self, application: Any) -> None: ...
    def file_path(self, url: Any): ...
    def serve(self, request: Any) -> FileResponse: ...

class _StaticFilesHandler(FSFilesHandler):
    def get_base_dir(self): ...
    def get_base_url(self): ...

class _MediaFilesHandler(FSFilesHandler):
    def get_base_dir(self): ...
    def get_base_url(self): ...

class LiveServerThread(threading.Thread):
    host: str = ...
    port: int = ...
    is_ready: threading.Event = ...
    error: Optional[ImproperlyConfigured] = ...
    static_handler: Type[WSGIHandler] = ...
    connections_override: Dict[str, BaseDatabaseWrapper] = ...
    def __init__(
        self,
        host: str,
        static_handler: Type[WSGIHandler],
        connections_override: Dict[str, BaseDatabaseWrapper] = ...,
        port: int = ...,
    ) -> None: ...
    httpd: ThreadedWSGIServer = ...
    def terminate(self) -> None: ...

class LiveServerTestCase(TransactionTestCase):
    host: str = ...
    port: int = ...
    server_thread_class: Type[Any] = ...
    server_thread: Any
    static_handler: Any = ...
    @classproperty
    def live_server_url(cls) -> str: ...
    @classproperty
    def allowed_host(cls) -> str: ...

class SerializeMixin:
    lockfile: Any = ...
    @classmethod
    def setUpClass(cls) -> None: ...
    @classmethod
    def tearDownClass(cls) -> None: ...

def connections_support_transactions(aliases: Optional[Iterable[str]] = ...) -> bool: ...
