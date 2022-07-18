class EventBus:

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
