import cv2
import numpy as np
import mediapipe as mp
import speech_recognition as sr
import threading
import pyttsx3
import time

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Global variables
canvas = None
temp_canvas = None
prev_x, prev_y = None, None
mode = "paint"  # Default mode is "paint"
color = (255, 0, 0)  # Default color (Blue)
thickness = 4  # Default line thickness
shape_drawing = False  # Flag to finalize shapes
pause_start_time = None  # Track pause start time
pause_threshold = 1.0  # Pause threshold in seconds
movement_threshold = 10  # Lower sensitivity for detecting movement

def speak(text):
    """Uses TTS to announce the current mode."""
    engine.say(text)
    engine.runAndWait()

def switch_mode(command):
    global mode, color, thickness
    if command == "paint":
        mode = "paint"
    elif command == "straight":
        mode = "straight"
    elif command == "erase":
        mode = "erase"
    elif command == "clear":
        mode = "clear"
        clear_canvas()
    elif command == "circle":
        mode = "circle"
    elif command == "rectangle":
        mode = "rectangle"
    elif command == "pink":
        color = (255, 105, 180)
    elif command == "green":
        color = (0, 255, 0)
    elif command == "blue":
        color = (255, 0, 0)
    elif command == "thicker":
        thickness = min(thickness + 2, 10)  # Max thickness 10
    elif command == "thinner":
        thickness = max(thickness - 2, 1)  # Min thickness 1

    speak(f"Switched to {command.replace('_', ' ')} mode")

def clear_canvas():
    """Clears the canvas to a blank image of the same resolution."""
    global canvas
    if canvas is not None:
        canvas.fill(0)

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            if command in ["paint", "straight", "erase", "clear", "circle", "rectangle", "pink", "green", "blue", "thicker", "thinner"]:
                switch_mode(command)
            else:
                print("Unknown command.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results; check your internet connection.")

def listen_for_commands_in_background():
    while True:
        listen_for_command()

def resize_with_aspect_ratio(image, width=None, height=None):
    """Resizes an image while maintaining its aspect ratio."""
    (h, w) = image.shape[:2]
    if width is not None:
        r = width / float(w)
        dim = (width, int(h * r))
    elif height is not None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        return image
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def main():
    global prev_x, prev_y, mode, canvas, temp_canvas, shape_drawing, pause_start_time
    cap = cv2.VideoCapture(0)
    
    # Set high resolution for the camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Define canvas size based on camera resolution
    frame_width = 1280
    frame_height = 720
    canvas = np.zeros((frame_height, frame_width, 3), dtype="uint8")
    temp_canvas = np.zeros((frame_height, frame_width, 3), dtype="uint8")  # Temporary canvas for shapes
    
    # Define camera frame size within the window
    cam_frame_size = (200, 150)  # Width and height of the camera frame

    # Start a separate thread to listen for commands
    threading.Thread(target=listen_for_commands_in_background, daemon=True).start()

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    h, w, _ = frame.shape
                    cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                    # Detect pause based on finger position
                    if prev_x is not None and prev_y is not None and (abs(cx - prev_x) < movement_threshold and abs(cy - prev_y) < movement_threshold):
                        if pause_start_time is None:
                            pause_start_time = time.time()
                        elif time.time() - pause_start_time > pause_threshold:
                            print("Pause detected in drawing.")
                            if mode in ["straight", "circle", "rectangle"]:
                                shape_drawing = False  # Finalize shape
                                canvas = cv2.add(canvas, temp_canvas)
                                temp_canvas.fill(0)  # Clear temporary canvas
                    else:
                        pause_start_time = None

                    # Mode-specific behavior
                    if mode == "paint":
                        if prev_x is not None and prev_y is not None:
                            cv2.line(canvas, (prev_x, prev_y), (cx, cy), color, thickness, lineType=cv2.LINE_AA)
                        prev_x, prev_y = cx, cy

                    elif mode == "straight":
                        if shape_drawing:
                            temp_canvas.fill(0)  # Clear temp canvas
                            cv2.line(temp_canvas, (prev_x, prev_y), (cx, cy), color, thickness, lineType=cv2.LINE_AA)
                        else:
                            prev_x, prev_y = cx, cy
                            shape_drawing = True

                    elif mode == "circle":
                        if shape_drawing:
                            temp_canvas.fill(0)
                            radius = int(np.sqrt((cx - prev_x) ** 2 + (cy - prev_y) ** 2))
                            cv2.circle(temp_canvas, (prev_x, prev_y), radius, color, thickness, lineType=cv2.LINE_AA)
                        else:
                            prev_x, prev_y = cx, cy
                            shape_drawing = True

                    elif mode == "rectangle":
                        if shape_drawing:
                            temp_canvas.fill(0)
                            cv2.rectangle(temp_canvas, (prev_x, prev_y), (cx, cy), color, thickness, lineType=cv2.LINE_AA)
                        else:
                            prev_x, prev_y = cx, cy
                            shape_drawing = True

                    elif mode == "erase":
                        cv2.circle(canvas, (cx, cy), 20, (0, 0, 0), -1)

                    # Draw hand landmarks on the screen for visual feedback
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            else:
                if mode in ["straight", "circle", "rectangle"] and shape_drawing:
                    shape_drawing = False  # Finalize shape on finger lift
                    canvas = cv2.add(canvas, temp_canvas)  # Add shape to main canvas
                    temp_canvas.fill(0)  # Clear temp canvas
                prev_x, prev_y = None, None
                pause_start_time = None

            # Combine the canvas with temp_canvas for live drawing
            combined_canvas = cv2.add(canvas, temp_canvas)

            # Resize the camera frame to fit in the top right corner
            resized_cam_frame = cv2.resize(frame, cam_frame_size, interpolation=cv2.INTER_AREA)
            
            # Place the camera frame in the top right corner of the combined canvas
            combined_canvas[0:cam_frame_size[1], -cam_frame_size[0]:] = resized_cam_frame

            # Display the canvas
            cv2.imshow("Air canvas", combined_canvas)

            # Check if the window was closed
            if cv2.getWindowProperty("Air canvas", cv2.WND_PROP_VISIBLE) < 1:
                break

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cv2.namedWindow("Air canvas", cv2.WINDOW_NORMAL)  # Allows resizing
    main()
