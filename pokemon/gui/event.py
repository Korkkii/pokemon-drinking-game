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


class MoveCamera(Event):
    def __init__(self, direction=None, target=None):
        self.direction = direction
        self.target = target


class MoveCameraTarget(Event):
    def __init__(self, target):
        self.target = target


class ChangeMusic(Event):
    def __init__(self):
        pass


class PlayerMoved(Event):
    def __init__(self, player, from_square, to_square):
        self.player = player
        self.from_square = from_square
        self.to_square = to_square


class PlayTurn(Event):
    def __init__(self):
        pass
