"""
Virtual Mouse Using Hand Gestures
Controls:
  - Move index finger: move cursor
  - Pinch thumb + index finger: left click
  - Press Q in the camera window: quit
Safety:
  - Keep your hand visible and start with the cursor in a safe area.
  - Move the cursor to a screen corner to trigger PyAutoGUI's failsafe.
"""

import time
import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# -------------------- Settings you can change --------------------
CAMERA_INDEX = 0
FRAME_WIDTH = 960
FRAME_HEIGHT = 540
SMOOTHING = 5          # Higher = smoother, but slower
PINCH_THRESHOLD = 0.045  # Smaller = fingers must be closer
CLICK_COOLDOWN = 0.45  # Seconds between clicks
ACTIVE_MARGIN = 0.12   # Ignore the outer 12% of camera view
# -----------------------------------------------------------------

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():
    raise SystemExit(
        "Could not open webcam. Close other camera apps or change CAMERA_INDEX in main.py."
    )

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

previous_x, previous_y = 0, 0
last_click_time = 0.0
pinch_was_active = False
cursor_x, cursor_y = screen_width // 2, screen_height // 2

print("Virtual Mouse is running.")
print("Move your index finger to move the cursor.")
print("Pinch thumb + index finger to left-click.")
print("Press Q in the camera window to quit.")

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
) as hands:
    while True:
        success, frame = cap.read()
        if not success:
            print("Unable to read from webcam.")
            break

        # Mirror the frame so hand movement feels natural.
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        status = "Show one hand"
        status_color = (0, 220, 255)

        # Draw a guide rectangle for the useful tracking area.
        left = int(FRAME_WIDTH * ACTIVE_MARGIN)
        right = int(FRAME_WIDTH * (1 - ACTIVE_MARGIN))
        top = int(FRAME_HEIGHT * ACTIVE_MARGIN)
        bottom = int(FRAME_HEIGHT * (1 - ACTIVE_MARGIN))
        cv2.rectangle(frame, (left, top), (right, bottom), (80, 200, 80), 1)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )
            points = hand.landmark

            # Landmark 8 = index fingertip; landmark 4 = thumb tip.
            index_tip = points[8]
            thumb_tip = points[4]

            # Clamp fingertip position to the active area, then map to screen.
            nx = np.clip((index_tip.x - ACTIVE_MARGIN) / (1 - 2 * ACTIVE_MARGIN), 0, 1)
            ny = np.clip((index_tip.y - ACTIVE_MARGIN) / (1 - 2 * ACTIVE_MARGIN), 0, 1)
            target_x = int(nx * screen_width)
            target_y = int(ny * screen_height)

            # Smooth cursor movement to reduce small tracking jitters.
            cursor_x = previous_x + (target_x - previous_x) / SMOOTHING
            cursor_y = previous_y + (target_y - previous_y) / SMOOTHING
            previous_x, previous_y = cursor_x, cursor_y

            # Normalized distance between thumb and index fingertip.
            pinch_distance = np.hypot(
                thumb_tip.x - index_tip.x,
                thumb_tip.y - index_tip.y
            )
            pinch_active = pinch_distance < PINCH_THRESHOLD

            try:
                pyautogui.moveTo(int(cursor_x), int(cursor_y), _pause=False)
            except pyautogui.FailSafeException:
                print("Failsafe triggered. Exiting safely.")
                break

            if pinch_active:
                status = "PINCH: Left click"
                status_color = (50, 255, 50)
                now = time.time()
                # Click only when the pinch begins, not continuously while held.
                if not pinch_was_active and now - last_click_time >= CLICK_COOLDOWN:
                    try:
                        pyautogui.click()
                    except pyautogui.FailSafeException:
                        print("Failsafe triggered. Exiting safely.")
                        break
                    last_click_time = now
            else:
                status = "Tracking hand"
                status_color = (255, 220, 80)

            pinch_was_active = pinch_active

            cv2.circle(
                frame,
                (int(index_tip.x * FRAME_WIDTH), int(index_tip.y * FRAME_HEIGHT)),
                10,
                (255, 0, 255),
                cv2.FILLED,
            )
        else:
            pinch_was_active = False

        cv2.rectangle(frame, (0, 0), (FRAME_WIDTH, 82), (25, 25, 25), cv2.FILLED)
        cv2.putText(
            frame, "VIRTUAL MOUSE", (18, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )
        cv2.putText(
            frame, status, (18, 62),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2
        )
        cv2.putText(
            frame, "Index finger = move | Pinch = click | Q = quit",
            (18, FRAME_HEIGHT - 18),
            cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1
        )

        cv2.imshow("Virtual Mouse - Hand Gesture Control", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

cap.release()
cv2.destroyAllWindows()
print("Virtual Mouse closed.")
