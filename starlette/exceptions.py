import http
import typing
import warnings

__all__ = ("HTTPException",)


class HTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: typing.Optional[str] = None,
        headers: typing.Optional[dict] = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"

    def __reduce__(self) -> typing.Tuple[typing.Any, ...]:
        return type(self), (self.status_code, self.detail, self.headers)


__deprecated__ = "ExceptionMiddleware"


def __getattr__(name: str) -> typing.Any:  # pragma: no cover
    if name == __deprecated__:
        from starlette.middleware.exceptions import ExceptionMiddleware

        warnings.warn(
            f"{__deprecated__} is deprecated on `starlette.exceptions`. "
            f"Import it from `starlette.middleware.exceptions` instead.",
            category=DeprecationWarning,
            stacklevel=3,
        )
        return ExceptionMiddleware
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> typing.List[str]:
    return sorted(list(__all__) + [__deprecated__])  # pragma: no cover
