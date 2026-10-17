# Virtual Mouse Using Hand Gestures

A beginner-friendly computer vision project that controls the mouse using a laptop webcam.

## Features
- Live webcam with hand landmarks
- Move the cursor using the index fingertip
- Left-click by pinching the thumb and index fingertip together
- Cursor smoothing
- On-screen status and quit key

## Requirements
- Python 3.10 or 3.11 is a good starting point. MediaPipe support varies by Python version.
- Laptop webcam
- Windows, macOS, or Linux desktop session
- Internet connection for the first-time package installation

## Setup (Windows)
1. Extract this ZIP to a folder.
2. Install Python 3.10 or 3.11 (64-bit) if needed. During installation, enable **Add Python to PATH**.
3. Open the project folder.
4. Click the folder address bar, type `cmd`, and press Enter.
5. Create a virtual environment:

   ```bash
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   ```

   If your computer uses `python` instead of `py -3.11`, run `python -m venv .venv` instead.

6. Install the libraries:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Start the app:

   ```bash
   python main.py
   ```

8. Keep your hand in view. Move your index finger to move the cursor. Pinch your thumb and index finger together to left-click.
9. Press **Q** in the camera window to exit.

## Setup (macOS/Linux)
Create and activate a virtual environment, then install packages:

```bash
python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

macOS may ask for Camera and Accessibility permissions. Linux needs a graphical desktop session; Wayland may restrict global mouse control depending on the desktop environment.

## Controls
- **Index fingertip:** cursor movement
- **Thumb + index pinch:** left-click
- **Q** or **Esc:** quit

## Troubleshooting
- **Camera won't open:** close Zoom/Teams/browser camera tabs, then try changing `CAMERA_INDEX = 0` to `1` in `main.py`.
- **No module named mediapipe:** make sure the virtual environment is activated and install from `requirements.txt`.
- **Cursor too shaky:** increase `SMOOTHING` in `main.py` (for example, 7). Higher values feel slower.
- **Clicks happen too easily:** reduce `PINCH_THRESHOLD` (for example, `0.035`). If clicks are not detected, try `0.055`.
- **Cursor moves too slowly:** lower `SMOOTHING` (for example, 3).
- **PyAutoGUI failsafe:** moving the cursor to a screen corner can stop the program. This is a safety feature.
- **Camera permissions:** allow your terminal/Python app to use the camera.

## Safety and privacy
- Video is processed locally; this starter project does not upload or save camera footage.
- Test with a blank desktop first, and keep important documents closed.
- Cursor movement and clicks affect the real computer. Press **Q** in the camera window to quit.
- Do not use this prototype for security-sensitive actions or accessibility-critical tasks without further testing.

## How it works
1. OpenCV reads webcam frames.
2. MediaPipe finds hand landmarks.
3. The index fingertip position is mapped to screen coordinates.
4. PyAutoGUI moves the mouse.
5. The distance between thumb and index fingertips determines whether a pinch click occurred.
