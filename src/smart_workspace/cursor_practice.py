from math import dist

import cv2
from cv2.typing import MatLike

from smart_workspace.cursor_mapping import map_to_screen


CAMERA_BOX = (0.25, 0.25, 0.75, 0.75)
TARGETS = ((0.18, 0.22), (0.82, 0.22), (0.50, 0.50), (0.18, 0.78), (0.82, 0.78))
TARGET_RADIUS = 14
BACKGROUND = (34, 29, 25)
CURSOR_COLOR = (210, 230, 86)
TARGET_COLOR = (151, 142, 132)
HOVER_COLOR = (116, 219, 137)
TEXT_COLOR = (230, 226, 220)


def draw_cursor_practice(
    frame: MatLike, fingertip: tuple[float, float] | None
) -> MatLike:
    height, width = frame.shape[:2]
    left, top, right, bottom = CAMERA_BOX
    cv2.rectangle(
        frame,
        (round(left * width), round(top * height)),
        (round(right * width), round(bottom * height)),
        CURSOR_COLOR,
        2,
        cv2.LINE_AA,
    )

    panel = frame.copy()
    panel[:] = BACKGROUND
    cursor = None
    if fingertip is not None:
        cursor = map_to_screen(fingertip, CAMERA_BOX, (width, height))

    for x, y in TARGETS:
        center = (round(x * (width - 1)), round(y * (height - 1)))
        hovered = cursor is not None and dist(cursor, center) <= TARGET_RADIUS
        color = HOVER_COLOR if hovered else TARGET_COLOR
        thickness = cv2.FILLED if hovered else 2
        cv2.circle(panel, center, TARGET_RADIUS, color, thickness, cv2.LINE_AA)

    cv2.putText(
        panel, "Cursor practice", (16, 26), cv2.FONT_HERSHEY_SIMPLEX,
        0.6, TEXT_COLOR, 1, cv2.LINE_AA,
    )
    if cursor is None:
        cv2.putText(
            panel, "Show one hand", (16, height - 14), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, TEXT_COLOR, 1, cv2.LINE_AA,
        )
    else:
        cv2.circle(panel, cursor, 8, BACKGROUND, cv2.FILLED, cv2.LINE_AA)
        cv2.circle(panel, cursor, 5, CURSOR_COLOR, cv2.FILLED, cv2.LINE_AA)

    return cv2.hconcat([frame, panel])
