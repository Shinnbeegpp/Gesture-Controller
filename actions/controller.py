import pyautogui


def toggle_play_pause():
    print("ACTION: Toggling Play/Pause")
    pyautogui.press('playpause')

def volume_up():
    print("ACTION: Volume Up")
    pyautogui.press('volumeup')

def volume_down():
    print("ACTION: Volume Down")
    pyautogui.press('volumedown')

def next_track():
    print("ACTION: Next Track")
    pyautogui.press('nexttrack')

def previous_track():
    print("ACTION: Previous Track")
    pyautogui.press('prevtrack')


