from math import dist


PINCH_THRESHOLD = 0.30


def detect_pinch(points: list[tuple[int, int]]) -> tuple[bool, float] | None:
    """Return whether the hand is pinching and its gap-to-palm-width ratio."""
    thumb_tip, index_tip = points[4], points[8]
    index_knuckle, pinky_knuckle = points[5], points[17]
    palm_width = dist(index_knuckle, pinky_knuckle)
    if palm_width == 0:
        return None

    ratio = dist(thumb_tip, index_tip) / palm_width
    return ratio < PINCH_THRESHOLD, ratio
