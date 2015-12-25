from pygame import Rect


class Camera:
    def __init__(self, camera_function, level_size, window_size):
        self.camera_function = camera_function
        self.state = Rect(0, 0, level_size[0], level_size[1])
        self.window_width, self.window_height = window_size
        # self.window_height = window_height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_function(target.rect)


class FollowFocusCamera(Camera):
    def __init__(self, level_size, window_size):
        Camera.__init__(self, self.camera_function_follow, level_size, window_size)

    def camera_function_follow(self, target_rectangle):
        x, y, _, _ = target_rectangle  # x = from left, y = from top
        _, _, w, h = self.state  # w = width, h = height
        x, y, _, _ = -x + int(self.window_width / 2), -y + int(self.window_height / 2), w, h

        x = max(-(self.state.width - self.window_width), x)
        x = min(0, x)
        y = max(-(self.state.height - self.window_height), y)
        y = min(0, y)
        # y = max(-(self.state.width - self.window_width), min(0, y))  # Stop scrolling at left / right edges
        # x = min(0, max(-(self.state.height - self.window_height), x))  # Stop scrolling at top / bottom edges
        return Rect(x, y, w, h)
