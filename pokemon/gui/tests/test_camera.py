from pokemon.gui.camera import FollowFocusCamera


def test_camera_init():
    """
    """
    level_size = (400, 300)
    window_size = (1920, 1080)
    start_points = [(-1, -1), (0, 0), (1, 1), (200, 150),
                    (399, 149), (400, 300), (430, 330)]
    for start_point in start_points:
        camera = FollowFocusCamera(start_point[0], start_point[1],
                                   level_size, window_size)
        assert 0 <= camera.state.x <= level_size[0], \
            "Camera x coordinate expected to be within 0 and level width {}, but was {}".format(
            level_size[0], camera.state.x)
        assert 0 <= camera.state.y <= level_size[1], \
            "Camera y coordinate expected to be within 0 and level height {}, but was {}".format(
            level_size[1], camera.state.y)


def test_camera_movement():
    level_size = (400, 300)
    window_size = (1920, 1080)
    start_points = [(0, 0), (30, 30), (200, 150),
                    (370, 120), (400, 300)]
    movements = [(0, 0), (30, 0), (0, 30), (-30, 0), (0, -30)]
    for start_point in start_points:
        for movement in movements:
            camera = FollowFocusCamera(start_point[0], start_point[1],
                                       level_size, window_size)
            camera.camera_function_follow(movement)
            assert 0 <= camera.state.x <= level_size[0], \
                "Camera x coordinate expected to be within 0 and level width {}, but was {}".format(
                level_size[0], camera.state.x)

            assert 0 <= camera.state.y <= level_size[1], \
                "Camera y coordinate expected to be within 0 and level height {}, but was {}".format(
                level_size[1], camera.state.y)
