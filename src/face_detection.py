 
import cv2
import dlib
import time  # Import time module to add delays

# Load pre-trained models (ensure you update the path if needed)
predictor_path = "../data/dataset/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()

try:
    predictor = dlib.shape_predictor(predictor_path)
except RuntimeError as e:
    print(f"Error loading shape predictor: {e}")
    exit()

def detect_face_expressions():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from camera")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) > 0:
            for face in faces:
                # Get facial landmarks
                landmarks = predictor(gray, face)

                # Here, we just return "smile" as a simple example
                # In a real scenario, you can analyze the landmarks for expression detection
                return "smile"  # This could be more advanced, e.g., detecting facial features for expressions

        else:
            print("No face detected")

        # Display the frame with detected faces (optional for debugging)
        for face in faces:
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame with the face detected
        cv2.imshow("Face Detection", frame)

        # Add a small delay to give time for face detection
        time.sleep(1)  # Add 1 second delay to allow more time for the face to be detected

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close any open windows
    cap.release()
    cv2.destroyAllWindows()

# Start the face detection and expression recognition
if __name__ == "__main__":
    try:
        expression = detect_face_expressions()
        print(f"Detected expression: {expression}")
    except Exception as e:
        print(f"An error occurred: {e}")
