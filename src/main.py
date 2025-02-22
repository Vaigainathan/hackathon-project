from face_detection import detect_face_expressions
from voice_recognition import recognize_voice_commands
from intent_recognition import recognize_intent
from action_execution import perform_action
import time

def map_intent_to_action(intent):
    """ Maps recognized intent to an action """
    intent_map = {
        "open_app": "open_app",
        "scroll_up": "scroll_up",
        "terminate": "terminate"
    }
    return intent_map.get(intent, "unknown")

def start_interaction():
    print("System Ready! Please interact with the system.")
    
    while True:
        # Capture inputs
        face_expression = detect_face_expressions()
        voice_command = recognize_voice_commands()

        # Process inputs with AI
        intent = recognize_intent(face_expression, voice_command)

        # Determine action
        action = map_intent_to_action(intent)

        # Perform action
        perform_action(action)

        # Provide feedback
        print(f"Action performed: {action}")

        # Check for session termination
        if action == "terminate":
            print("Terminating interaction...")
            break

        time.sleep(1)  # Delay to simulate real-time processing

if __name__ == "__main__":
    start_interaction()
