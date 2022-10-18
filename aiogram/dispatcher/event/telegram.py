from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from aiogram.dispatcher.middlewares.manager import MiddlewareManager

from ...filters.base import Filter
from ...types import TelegramObject
from .bases import REJECTED, UNHANDLED, MiddlewareType, SkipHandler
from .handler import CallbackType, FilterObject, HandlerObject

if TYPE_CHECKING:
    from aiogram.dispatcher.router import Router


class TelegramEventObserver:
    """
    Event observer for Telegram events

    Here you can register handler with filters or bounded filters which can be used as keyword arguments instead of writing full references when you register new handlers.
    This observer will stop event propagation when first handler is pass.
    """

    def __init__(self, router: Router, event_name: str) -> None:
        self.router: Router = router
        self.event_name: str = event_name

        self.handlers: List[HandlerObject] = []

        self.middleware = MiddlewareManager()
        self.outer_middleware = MiddlewareManager()

        # Re-used filters check method from already implemented handler object
        # with dummy callback which never will be used
        self._handler = HandlerObject(callback=lambda: True, filters=[])

    def filter(self, *filters: CallbackType) -> None:
        """
        Register filter for all handlers of this event observer

        :param filters: positional filters
        :param bound_filters: keyword filters
        """
        if self._handler.filters is None:
            self._handler.filters = []
        self._handler.filters.extend([FilterObject(filter_) for filter_ in filters])

    def _resolve_middlewares(self) -> List[MiddlewareType[TelegramObject]]:
        middlewares: List[MiddlewareType[TelegramObject]] = []
        for router in reversed(tuple(self.router.chain_head)):
            observer = router.observers[self.event_name]
            middlewares.extend(observer.middleware)

        return middlewares

    def register(
        self,
        callback: CallbackType,
        *filters: CallbackType,
        flags: Optional[Dict[str, Any]] = None,
    ) -> CallbackType:
        """
        Register event handler
        """
        if flags is None:
            flags = {}

        for item in filters:
            if isinstance(item, Filter):
                item.update_handler_flags(flags=flags)

        self.handlers.append(
            HandlerObject(
                callback=callback,
                filters=[FilterObject(filter_) for filter_ in filters],
                flags=flags,
            )
        )

        return callback

    def wrap_outer_middleware(
        self, callback: Any, event: TelegramObject, data: Dict[str, Any]
    ) -> Any:
        wrapped_outer = self.middleware.wrap_middlewares(
            self.outer_middleware,
            callback,
        )
        return wrapped_outer(event, data)

    async def trigger(self, event: TelegramObject, **kwargs: Any) -> Any:
        """
        Propagate event to handlers and stops propagation on first match.
        Handler will be called when all its filters is pass.
        """
        # Check globally defined filters before any other handler will be checked
        result, data = await self._handler.check(event, **kwargs)
        if not result:
            return REJECTED
        kwargs.update(data)

        for handler in self.handlers:
            result, data = await handler.check(event, **kwargs)
            if result:
                kwargs.update(data, handler=handler)
                try:
                    wrapped_inner = self.outer_middleware.wrap_middlewares(
                        self._resolve_middlewares(),
                        handler.call,
                    )
                    return await wrapped_inner(event, kwargs)
                except SkipHandler:
                    continue

        return UNHANDLED

    def __call__(
        self,
        *filters: CallbackType,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[CallbackType], CallbackType]:
        """
        Decorator for registering event handlers
        """

        def wrapper(callback: CallbackType) -> CallbackType:
            self.register(callback, *filters, flags=flags)
            return callback

        return wrapper
