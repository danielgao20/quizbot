import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QShortcut
from PyQt5.QtGui import QGuiApplication, QKeySequence
from PyQt5.QtCore import Qt
import pytesseract
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")
client = OpenAI(api_key=api_key)

# Function to send text to GPT and get an answer
def chat_gpt(prompt):
    print("Sending text to GPT...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"Provide a concise and clear answer: {prompt}"}
            ],
        )
        print("Received response from GPT.")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Failed to get answer from GPT:", e)
        return None

# Function to capture the entire screen
def capture_screenshot():
    print("Capturing screenshot...")
    try:
        screen = QGuiApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        screenshot_path = "screenshot.png"
        pixmap.save(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}.")
        return screenshot_path
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
        return None

# Function to process the screenshot and extract text
def process_screenshot(image_path):
    print(f"Processing screenshot at {image_path}...")
    try:
        extracted_text = pytesseract.image_to_string(image_path)
        print(f"Extracted text: {extracted_text}...")
        return extracted_text.strip()
    except Exception as e:
        print(f"Failed to process screenshot: {e}")
        return None

# Function to display the answer in a transparent overlay
def display_answer(answer, overlay_label):
    print("Displaying answer...")
    if answer:
        overlay_label.setText(answer)
        overlay_label.adjustSize()
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        overlay_label.move(
            screen_geometry.width() - overlay_label.width() - 10,
            screen_geometry.height() - overlay_label.height() - 10
        )
        print(f"Answer displayed: {answer}")
    else:
        print("No answer to display.")

# Function to toggle the visibility of the answer
def toggle_answer(overlay_label, toggle_button):
    if overlay_label.isVisible():
        overlay_label.hide()
        toggle_button.setText("Light")
    else:
        overlay_label.show()
        toggle_button.setText("Dark")

# Main function to handle the workflow
def handle_workflow(overlay_label):
    print("Workflow triggered.")
    screenshot_path = capture_screenshot()
    if not screenshot_path:
        print("Screenshot capture failed.")
        return

    extracted_text = process_screenshot(screenshot_path)
    if not extracted_text:
        print("No text extracted from the screenshot.")
        overlay_label.setText("No text found.")
        overlay_label.show()
        return

    answer = chat_gpt(extracted_text)
    if answer:
        display_answer(answer, overlay_label)
    else:
        print("No answer returned from GPT.")
        overlay_label.setText("No answer found.")
        overlay_label.show()

# Create the application
def main():
    print("Starting application...")
    app = QApplication(sys.argv)

    overlay_label = QLabel()
    overlay_label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    overlay_label.setAttribute(Qt.WA_TranslucentBackground)
    overlay_label.setStyleSheet("color: lightgrey; background: rgba(0, 0, 0, 0); font-size: 6px;")
    overlay_label.setAlignment(Qt.AlignLeft)
    print("Overlay label created.")

    button = QPushButton("BUAD 310")
    button.setFixedSize(100, 50)
    button.setStyleSheet("background: rgba(0, 0, 0, 0); color: lightgrey; font-size: 10px; border: none;")
    button.setToolTip("Click to capture the screen and process the quiz.")
    button.clicked.connect(lambda: handle_workflow(overlay_label))
    button.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    button.move(10, QApplication.primaryScreen().geometry().height() - 100)  # bottom-left corner
    button.show()
    print("Button created and shown.")

    toggle_button = QPushButton("Light")
    toggle_button.setFixedSize(100, 50)
    toggle_button.setStyleSheet("background: rgba(0, 0, 0, 0); color: lightgrey; font-size: 10px; border: none;")
    toggle_button.setToolTip("Toggle answer visibility.")
    toggle_button.clicked.connect(lambda: toggle_answer(overlay_label, toggle_button))
    toggle_button.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    toggle_button.move(QApplication.primaryScreen().geometry().width() - 150, -30)  # top-right corner
    toggle_button.show()
    print("Toggle button created and shown.")

    # Add a keyboard shortcut (Command+Shift+C) for capturing the quiz, doesn't work yet
    shortcut = QShortcut(QKeySequence("Meta+Shift+C"), button)
    shortcut.activated.connect(lambda: handle_workflow(overlay_label))
    print("Shortcut (Command+Shift+C) connected.")

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
