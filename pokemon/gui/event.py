from weakref import WeakKeyDictionary


class Event:
    """
    A superclass for all events that can be sent to EventManager
    """


class EventManager:
    """
    Communication mediator between the Model, View, and Controller (MVC-model)
    """

    def __init__(self):
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post_event(self, event):
        for listener in self.listeners.keys():
            listener.notify(event)


class TickEvent(Event):
    def __init__(self):
        pass


class QuitEvent(Event):
    def __init__(self):
        pass
