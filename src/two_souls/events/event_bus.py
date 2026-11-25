from collections.abc import Callable
from typing import Any


class EventBus:
    """Manages event subscriptions and event publishing."""

    def __init__(self) -> None:
        self._subscribers: dict[
            type,
            list[Callable[[Any], None]]
        ] = {}

    def subscribe(
        self,
        event_type: type,
        handler: Callable[[Any], None]
    ) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: object) -> None:
        event_type = type(event)

        handlers = self._subscribers.get(event_type, ())

        for handler in tuple(handlers):
            handler(event)