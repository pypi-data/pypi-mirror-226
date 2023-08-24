from typing import List, Any, Callable

from reactivex import Observer, operators
from reactivex.abc import DisposableBase
from reactivex.disposable import CompositeDisposable, Disposable
import logging
import traceback
import sys


def never_ending_observer(
    on_next: Callable[[Any], None], name: str, logger: logging.Logger
):
    """Returns an OnNext only observer which logs an error to `logger` if it ever completes or errors"""
    return Observer(
        on_next=on_next,
        on_error=lambda exc: logger.error(f"Unexpected error in {name}: %s", exc),
        on_completed=lambda: logger.error(f"Unexpected completion in {name}"),
    )


def debug_observer(prefix: str, logger_name: str = "") -> Observer[Any]:
    logger_ = logging.getLogger(logger_name)

    def fn(x, scope):
        logger_.debug(f"[{prefix}][{scope}] - {x}")
        if scope == "ERROR":
            traceback.print_exception(*sys.exc_info())

    return Observer(
        lambda x: fn(x, "NEXT"),
        lambda x: fn(x, "ERROR"),
        lambda: fn("No message on completion", "COMPLETE"),
    )


def debug_operator(prefix: str, logger_name: str = ""):
    return operators.do(debug_observer(prefix, logger_name=logger_name))


def info_observer(prefix: str, logger_name: str = "") -> Observer[Any]:
    logger_ = logging.getLogger(logger_name)

    def fn(x, scope):
        c = (
            logger_.warning
            if scope == "COMPLETE"
            else logger_.error
            if scope == "ERROR"
            else logger_.info
        )
        c(f"[{prefix}] - {x}")
        if scope == "ERROR":
            traceback.print_exception(*sys.exc_info())

    return Observer(
        lambda x: fn(x, "NEXT"),
        lambda x: fn(x, "ERROR"),
        lambda: fn("Completed", "COMPLETE"),
    )


def info_operator(prefix: str, logger_name: str = ""):
    return operators.do(info_observer(prefix, logger_name=logger_name))


class LogOnDisposeDisposable(CompositeDisposable):
    def __init__(
        self,
        disposables: List[DisposableBase],
        message: str = "",
        logger_name: str = "",
    ):
        logger_ = logging.getLogger(logger_name)
        super().__init__(
            *disposables,
            Disposable(action=lambda: logger_.info("DISPOSING %s", message)),
        )
