import time
from pathlib import Path

import cv2
import mediapipe as mp

from smart_workspace.gestures import detect_pinch


def main() -> None:
    vision = mp.tasks.vision
    model_path = Path(__file__).resolve().with_name("hand_landmarker.task")
    options = vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )
    hand_connections = vision.HandLandmarksConnections.HAND_CONNECTIONS

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera.release()
        raise RuntimeError("Could not open camera 0")

    try:
        with vision.HandLandmarker.create_from_options(options) as landmarker:
            while True:
                success, frame = camera.read()
                if not success:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                timestamp_ms = time.monotonic_ns() // 1_000_000
                result = landmarker.detect_for_video(mp_image, timestamp_ms)

                frame_height, frame_width = frame.shape[:2]
                pinch_results = []
                for hand_landmarks in result.hand_landmarks:
                    points = [
                        (int(landmark.x * frame_width), int(landmark.y * frame_height))
                        for landmark in hand_landmarks
                    ]
                    for connection in hand_connections:
                        cv2.line(
                            frame,
                            points[connection.start],
                            points[connection.end],
                            (0, 255, 0),
                            2,
                        )
                    for point in points:
                        cv2.circle(frame, point, 4, (0, 165, 255), -1)
                    pinch_results.append(detect_pinch(points))

                for hand_number, pinch in enumerate(pinch_results, start=1):
                    if pinch is None:
                        continue
                    is_pinching, ratio = pinch
                    status = "PINCH" if is_pinching else "NO PINCH"
                    label = f"Hand {hand_number}: {status} ({ratio:.2f})"
                    label_y = 28 * hand_number
                    cv2.rectangle(frame, (6, label_y - 21), (250, label_y + 4), (0, 0, 0), -1)
                    cv2.putText(
                        frame,
                        label,
                        (12, label_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )

                cv2.imshow("Hand Landmarker", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
