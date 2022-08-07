class EventBus:
    """
    A simple event management class for Event Driven Patterns
    Use EventBus.get_global_instance if you're intending to use a global event system
    Otherwise, you can initiate an instance: event_bus = EventBus()
    event_bus.subscribe('event_occurred', event_handler) # registers function:'event_handler' to event:'event_occurred'
    event_bus.fire_event('event_occurred', arg0, arg1=val1) # fires an event called 'event_occurred'
    """
    _instance = None

    def __init__(self) -> None:
        super().__init__()
        self._listeners_map = {}

    def fire_event(self, event, *args, **kwargs):
        for listener_func in self._listeners_map[event]:
            listener_func(*args, **kwargs)

    def subscribe(self, event, listener_func):
        if event not in self._listeners_map:
            self._listeners_map[event] = []
        self._listeners_map[event].append(listener_func)

    def unsubscribe(self, event, listener_func):
        if event not in self._listeners_map:
            self._listeners_map[event].remove(listener_func)

    @staticmethod
    def get_global_instance():
        if EventBus._instance == None:
            EventBus._instance = EventBus()
        return EventBus._instance
