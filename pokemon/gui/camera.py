from pygame import Rect


class Camera:
    def __init__(self, camera_function, level_width, level_height, window_size):
        self.camera_function = camera_function
        self.state = Rect(0, 0, level_width, level_height)
        self.window_width, self.window_height = window_size
        # self.window_height = window_height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_function(target.rect)


class FollowFocusCamera(Camera):
    def __init__(self, level_width, level_height, window_size):
        Camera.__init__(self, self.camera_function_follow, level_width, level_height, window_size)

    def camera_function_follow(self, target_rectangle):
        x, y, _, _ = target_rectangle  # x = from left, y = from top
        _, _, w, h = self.state  # w = width, h = height
        x, y, _, _ = -x + int(self.window_width / 2), -y + int(self.window_height / 2), w, h
        # x = max(-(self.state.width - self.window_width), min(0, x))  # Stop scrolling at left / right edges
        # y = min(0, max(-(self.state.height - self.window_height), y))  # Stop scrolling at top / bottom edges
        return Rect(x, y, w, h)
