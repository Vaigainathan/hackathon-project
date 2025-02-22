import cv2
import dlib
import os
import time
import numpy as np
import action_execution  # Import action execution module

# Load the model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICTOR_PATH = os.path.join(BASE_DIR, "../data/datasets/shape_predictor_68_face_landmarks.dat")

detector = dlib.get_frontal_face_detector()

# Ensure model exists
if not os.path.exists(PREDICTOR_PATH):
    print(f"Error: Model file not found at {PREDICTOR_PATH}.")
    exit()

predictor = dlib.shape_predictor(PREDICTOR_PATH)

# Initialize baseline values
baseline_values = {
    "brow_height": None,
    "eye_openness": None,
    "nose_x": None,
    "jaw_y": None,
    "nose_y": None
}

last_action_times = {
    "scroll": 0,
    "close": 0,
    "head_turn": 0
}

# Calibration Function
def calibrate_face(cap):
    print("Calibrating... Keep a neutral expression for 5 seconds.")
    temp_values = {key: [] for key in baseline_values}
    
    for _ in range(50):  # Capture more frames for better calibration
        ret, frame = cap.read()
        if not ret:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if faces:
            face = faces[0]
            landmarks = predictor(gray, face)
            
            temp_values["brow_height"].append((landmarks.part(21).y + landmarks.part(22).y) / 2)
            eye_top = (landmarks.part(37).y + landmarks.part(44).y) / 2
            eye_bottom = (landmarks.part(41).y + landmarks.part(46).y) / 2
            temp_values["eye_openness"].append(eye_bottom - eye_top)
            temp_values["nose_x"].append(landmarks.part(30).x)
            temp_values["nose_y"].append(landmarks.part(30).y)
            temp_values["jaw_y"].append(landmarks.part(8).y)
    
    for key in temp_values:
        baseline_values[key] = np.mean(temp_values[key])  # Average for stability
    
    print("Calibration complete! Start making expressions.")

def detect_face_expressions():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    calibrate_face(cap)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Frame not captured.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        for face in faces:
            landmarks = predictor(gray, face)
            
            current_values = {
                "brow_height": (landmarks.part(21).y + landmarks.part(22).y) / 2,
                "eye_openness": (landmarks.part(41).y + landmarks.part(46).y) / 2 - (landmarks.part(37).y + landmarks.part(44).y) / 2,
                "nose_x": landmarks.part(30).x,
                "nose_y": landmarks.part(30).y,
                "jaw_y": landmarks.part(8).y
            }
            
            head_movement_x = current_values["nose_x"] - baseline_values["nose_x"]
            head_movement_y = current_values["nose_y"] - baseline_values["nose_y"]
            jaw_movement_y = current_values["jaw_y"] - baseline_values["jaw_y"]
            
            current_time = time.time()

            # Scroll Up/Down Based on Eyebrow Movement
            if current_time - last_action_times["scroll"] > 0.3:
                if current_values["brow_height"] < baseline_values["brow_height"] - 4:
                    action_execution.perform_action("scroll_down")
                    last_action_times["scroll"] = current_time
                elif current_values["brow_height"] > baseline_values["brow_height"] + 4:
                    action_execution.perform_action("scroll_up")
                    last_action_times["scroll"] = current_time
            
            # Close App When Looking Down + Jaw Drop
            if current_time - last_action_times["close"] > 2:
                if jaw_movement_y > 18 and head_movement_y > 15:
                    action_execution.perform_action("close_app")
                    last_action_times["close"] = current_time
            
            # Left/Right Head Movement for Page Navigation
            if current_time - last_action_times["head_turn"] > 1.5:
                if head_movement_x > 25:
                    action_execution.perform_action("go_forward")
                    last_action_times["head_turn"] = current_time
                elif head_movement_x < -25:
                    action_execution.perform_action("go_back")
                    last_action_times["head_turn"] = current_time
            
            # Draw face landmarks for debugging
            for i in range(68):
                x, y = landmarks.part(i).x, landmarks.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        
        cv2.imshow("Face Detection Debug", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_face_expressions()
