import pystray
from PIL import Image, ImageDraw
import os

def create_placeholder_icon():
    image = Image.new('RGB', (64, 64), color='black')
    dc = ImageDraw.Draw(image)
    dc.rectangle((32, 0, 64, 32), fill='gray')
    dc.rectangle((0, 32, 32, 64), fill='gray')
    return image

def on_quit(icon, item):
    print("SYSTEM: Shutting down...")
    icon.stop()
    os._exit(0)

def run_tray_app():
    icon_image = create_placeholder_icon()
    
    menu = pystray.Menu(
        pystray.MenuItem("Quit Gesture Controller", on_quit)
    )
    tray = pystray.Icon("GestureController", icon_image, "Gesture Controller", menu)

    print("GUI: System Tray Icon is running in the background.")
    tray.run()