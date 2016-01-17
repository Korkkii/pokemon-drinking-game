from pygame import Rect
from abc import ABCMeta, abstractmethod


class Camera(metaclass=ABCMeta):
    def __init__(self, x, y, level_size, window_size):
        # Bound the x and y initially within the level area
        x = max(0, min(level_size[0], x))
        y = max(0, min(level_size[1], y))

        self.state = Rect(x, y, level_size[0], level_size[1])
        self.window_width, self.window_height = window_size

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    @abstractmethod
    def move_up(self, amount):
        raise NotImplementedError

    @abstractmethod
    def move_down(self, amount):
        raise NotImplementedError

    @abstractmethod
    def move_left(self, amount):
        raise NotImplementedError

    def move_right(self, amount):
        raise NotImplementedError


class FollowFocusCamera(Camera):
    def __init__(self, x, y, level_size, window_size):
        Camera.__init__(self, x, y, level_size, window_size)

    def camera_function_follow(self, amount):
        # x, y, _, _ = target_rectangle  # x = from left, y = from top
        # print(x, y, self.state.x, self.state.y)
        x, y, w, h = self.state  # w = width, h = height

        # Update x coordinate
        x -= amount[0]
        x = max(-(self.state.width - self.window_width), x)
        x = min(0, x)

        # Update y coordinate
        y -= amount[1]
        y = max(-(self.state.height - self.window_height), y)
        y = min(0, y)

        return Rect(x, y, w, h)

    def target(self, target):
        self.state = self.camera_function_follow(target)

    def move_up(self, amount=(0, 0)):
        self.state = self.camera_function_follow((0, -30))

    def move_down(self, amount=(0, 0)):
        self.state = self.camera_function_follow((0, 30))

    def move_left(self, amount=(0, 0)):
        self.state = self.camera_function_follow((-30, 0))

    def move_right(self, amount=(0, 0)):
        self.state = self.camera_function_follow((30, 0))
