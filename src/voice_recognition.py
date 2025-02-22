 
import speech_recognition as sr
import time  # To add a small delay for better performance

def recognize_voice_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Adjust the recognizer settings
    recognizer.energy_threshold = 4000  # Increase the threshold for more sensitivity
    recognizer.dynamic_energy_threshold = True  # Automatically adjust energy threshold during runtime
    recognizer.pause_threshold = 1  # How long to wait for silence before considering the command complete

    with microphone as source:
        print("Listening... Please speak clearly.")
        
        # Adjust for ambient noise and increase the timeout (seconds)
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Calibrate for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Increased timeout and phrase time limit
            print("Recognizing...")
            
            # Attempt to recognize the voice
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return ""
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Example usage
if __name__ == "__main__":
    command = recognize_voice_commands()
    if command:
        print(f"Command received: {command}")
    else:
        print("No valid command received.")
