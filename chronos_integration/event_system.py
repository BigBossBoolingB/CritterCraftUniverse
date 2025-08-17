from collections import defaultdict
from typing import Callable, Any, DefaultDict

class EventManager:
    """
    A simple event manager to handle event-driven logic.
    This allows for loose coupling between different parts of the application.
    """
    def __init__(self):
        self._handlers: DefaultDict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        """
        Subscribe a handler to a specific event type.

        Args:
            event_type: The name of the event to subscribe to.
            handler: The function to call when the event is posted.
        """
        self._handlers[event_type].append(handler)

    def post(self, event_type: str, data: Any = None):
        """
        Post an event to all subscribed handlers.

        Args:
            event_type: The name of the event being posted.
            data: The data to pass to the event handlers.
        """
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                if data is not None:
                    handler(data)
                else:
                    handler()
