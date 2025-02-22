import speech_recognition as sr
import os

def recognize_voice_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        try:
            with microphone as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized Command: {command}")
            execute_voice_command(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand the command. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; check your internet connection. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def execute_voice_command(command):
    # List of applications and their corresponding system commands
    apps_to_open = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "settings": "start ms-settings:",
        "file explorer": "explorer.exe",
        "paint": "mspaint.exe",
        "snipping tool": "snippingtool.exe",
        "wordpad": "write.exe",
        "windows media player": "wmplayer.exe",
        "microsoft edge": "start msedge",
        "internet explorer": "iexplore.exe",  # Only if installed
        "vs code": "code",
        "code": "code"
    }

    # Check for each application in the command and open it
    opened_any_app = False
    for app, system_command in apps_to_open.items():
        if app in command:
            print(f"Opening {app.capitalize()}...")
            os.system(system_command)
            opened_any_app = True

    # Terminate command
    if "terminate" in command or "exit" in command:
        print("Terminating session...")
        exit()

    # If no known command is found
    if not opened_any_app:
        print("No recognizable app command found. Please try again.")

if __name__ == "_main_":
    recognize_voice_commands()