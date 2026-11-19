def map_to_screen(
    fingertip: tuple[float, float],
    camera_bounds: tuple[float, float, float, float],
    screen_size: tuple[int, int],
) -> tuple[int, int]:
    """Map a normalized camera point from (left, top, right, bottom) to pixels."""
    x, y = fingertip
    left, top, right, bottom = camera_bounds
    width, height = screen_size
    if left >= right or top >= bottom:
        raise ValueError("The camera bounds must have a positive width and height")
    if width < 1 or height < 1:
        raise ValueError("The screen size must have a positive width and height")

    x_fraction = (x - left) / (right - left)
    y_fraction = (y - top) / (bottom - top)
    screen_x = round(min(max(x_fraction, 0.0), 1.0) * (width - 1))
    screen_y = round(min(max(y_fraction, 0.0), 1.0) * (height - 1))
    return screen_x, screen_y
