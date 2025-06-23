# AIR CANVAS — The Future of Touchless Drawing 🎨🖌️

**AIR CANVAS** is a gesture-controlled virtual whiteboard that lets you draw shapes, lines, and freehand strokes using only your index finger and a webcam — no stylus or touchscreen required! It also responds to **voice commands** to switch modes, change colors, adjust thickness, and more — making it a hands-free, interactive experience.

> 🚀 Built using Python, OpenCV, MediaPipe, SpeechRecognition, and pyttsx3.

## 📌 Features

- ✋ **Touchless Drawing**: Real-time index finger tracking using MediaPipe
- 🎙️ **Voice Commands**: Switch between tools like paint, erase, clear, line, circle, rectangle, and adjust color/thickness
- 🟦 **Shape Detection**: Draws straight lines, circles, and rectangles with pause-to-finalize logic
- 📷 **Live Overlay**: Seamless integration of camera feed with canvas
- 🧠 **Modular Code**: Easy to extend for more gestures and commands
- 🗣️ **TTS Feedback**: Voice feedback using pyttsx3 when a mode is changed

---

## 🧪 Technologies Used

| **Technology**    | **Purpose **                                 |
|-------------------|----------------------------------------------|
| Python            | Core programming language                    |
| OpenCV            | Drawing canvas, camera feed, image overlay   |
| MediaPipe         | Hand tracking and landmark detection         |
| SpeechRecognition | Real-time voice command capture              |
| pyttsx3           | Text-to-Speech feedback                      |
| Numpy             | Image processing and array manipulation      |
| Threading         | Concurrent voice command listening           |

---

## ⚙️ How It Works

1. **Detect Index Finger**  
   MediaPipe detects your hand and pinpoints the index fingertip.

2. **Track & Draw**  
   The fingertip position is mapped to the canvas and strokes are drawn in real time.

3. **Voice-Controlled Modes**  
   Say commands like `"paint"`, `"circle"`, `"erase"`, `"clear"`, `"thicker"` etc. to switch tools or styles.

4. **Pause Detection**  
   When the finger is steady for over 1 second, the system finalizes the shape (useful for line, circle, rectangle).

5. **Canvas Display**  
   Final and temporary drawings are merged with the camera feed and displayed live.

---

## 🗣️ Available Voice Commands

| **Command** | **Action**               |
| ----------- | ------------------------ |
| `paint`     | Freehand drawing         |
| `straight`  | Draw straight line       |
| `circle`    | Draw circle              |
| `rectangle` | Draw rectangle           |
| `erase`     | Eraser tool              |
| `clear`     | Clears entire canvas     |
| `blue`      | Change color to blue     |
| `green`     | Change color to green    |
| `pink`      | Change color to pink     |
| `thicker`   | Increase brush thickness |
| `thinner`   | Decrease brush thickness |

---

## 🧠 Future Innovations

- Alphabet and symbol recognition via gesture classification
- Web-based version using TensorFlow.js and WebRTC
- Undo/Redo gesture macros
- Collaborative canvas via socket programming
- AR headset integration for real-world air drawing
- Voice-to-text-to-sketch module using AI

---

## ✅ Requirements

- Python 3.7+
- Webcam
- Microphone
- Internet Connection (for voice recognition)
- Required Libraries (check requirements.txt)

---

## 👨‍💻 Author
Kunal Sachdev
Passionate about human-computer interaction, computer vision, and building accessible tech.

🔗 [LinkedIn](https://www.linkedin.com/in/kunal-sachdev-1343ba1b7/)  
💻 [GitHub](https://github.com/kunalsachdev06)


`If you find this project useful or inspiring, feel free to ⭐️ the repo and contribute ideas via issues or pull requests!`
