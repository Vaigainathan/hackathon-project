 

def perform_action(action):
    if action == "open_app":
        print("Opening app...")
    elif action == "scroll_up":
        print("Scrolling up...")
    elif action == "terminate":
        print("Terminating session...")
    else:
        print("Unknown action")
