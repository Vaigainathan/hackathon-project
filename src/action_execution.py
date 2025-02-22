import pyautogui
import time

def perform_action(action):
    if action == "scroll_up":
        print("Scrolling up...")
        pyautogui.scroll(200)  # Adjust scroll speed
    elif action == "scroll_down":
        print("Scrolling down...")
        pyautogui.scroll(-200)
    elif action == "go_forward":
        print("Navigating forward...")
        pyautogui.hotkey('alt', 'right')  # Forward navigation
    elif action == "go_back":
        print("Navigating backward...")
        pyautogui.hotkey('alt', 'left')  # Backward navigation
    elif action == "close_app":
        print("Closing application...")
        pyautogui.hotkey('alt', 'f4')  # Close window shortcut
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    # Test the module
    print("Testing actions...")
    time.sleep(2)  # Pause before executing
    perform_action("scroll_up")
    time.sleep(1)
    perform_action("scroll_down")
    time.sleep(1)
    perform_action("go_forward")
    time.sleep(1)
    perform_action("go_back")
    time.sleep(1)
    perform_action("close_app")
