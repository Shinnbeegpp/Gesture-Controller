import threading
from gui.tray_app import run_tray_app
from vision.hand_tracker import test_webcam_and_tracking

def start_vision_engine():
    print("SYSTEM: Spinning up Vision Engine thread...")

    vision_thread = threading.Thread(target=test_webcam_and_tracking, daemon=True)

    vision_thread.start()

if __name__ == "__main__":
    print("Booting Gesture Controller...")
    start_vision_engine()
    run_tray_app()
