"""
Desktop AI Buddy - Main Application
A free, open-source desktop AI companion with emotions, weather, and real-time chat
"""

import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt6.QtCore import QSize

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from ai_buddy import AIBuddy
from weather import WeatherManager
from emotions import EmotionManager, Emotion
from utils import get_current_time, get_greeting, get_full_date, ensure_dir_exists
import config


class AIResponseWorker(QThread):
    """Worker thread for AI responses"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, ai_buddy: AIBuddy, message: str, system_prompt: str):
        super().__init__()
        self.ai_buddy = ai_buddy
        self.message = message
        self.system_prompt = system_prompt
    
    def run(self):
        """Run AI chat in separate thread"""
        try:
            response = self.ai_buddy.chat(self.message, self.system_prompt)
            if response:
                self.response_ready.emit(response)
            else:
                self.error_occurred.emit("No response from AI")
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")


class DesktopAIBuddy(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.ai_buddy = AIBuddy(config.AI_MODEL, config.OLLAMA_HOST, config.OLLAMA_TIMEOUT)
        self.weather_manager = WeatherManager(config.LOCATION)
        self.emotion_manager = EmotionManager()
        
        # Setup UI
        self.init_ui()
        
        # Setup timers
        self.setup_timers()
        
        # Log startup
        ensure_dir_exists("logs")
        from utils import log_message
        log_message(f"Application started. AI Model: {config.AI_MODEL}")
    
    def init_ui(self):
        """Initialize user interface"""
        
        # Set window properties
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setGeometry(100, 100, config.BUDDY_WIDTH, config.BUDDY_HEIGHT)
        self.setStyleSheet(self.get_stylesheet())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # === Header ===
        header_layout = QHBoxLayout()
        
        # Buddy name and emoji
        self.buddy_label = QLabel(f"{config.BUDDY_NAME} {self.emotion_manager.get_emotion_emoji()}")
        self.buddy_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(self.buddy_label)
        
        header_layout.addStretch()
        
        # Time display
        self.time_label = QLabel(get_current_time())
        self.time_label.setFont(QFont("Arial", 10))
        self.time_label.setStyleSheet("color: #888;")
        header_layout.addWidget(self.time_label)
        
        main_layout.addLayout(header_layout)
        
        # === Greeting ===
        greeting_label = QLabel(get_greeting())
        greeting_label.setFont(QFont("Arial", 11))
        greeting_label.setStyleSheet("color: #666;")
        main_layout.addWidget(greeting_label)
        
        # === Weather Display ===
        self.weather_label = QLabel()
        self.weather_label.setFont(QFont("Arial", 9))
        self.weather_label.setStyleSheet("color: #888; background-color: #f0f0f0; padding: 8px; border-radius: 5px;")
        self.weather_label.setWordWrap(True)
        self.update_weather()
        main_layout.addWidget(self.weather_label)
        
        # === Chat Display Area ===
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 9))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.chat_display, 1)
        
        # === Input Area ===
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(60)
        self.input_field.setFont(QFont("Arial", 10))
        self.input_field.setPlaceholderText("Type your message here... (Shift+Enter to send)")
        self.input_field.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.input_field.keyPressEvent = self.handle_input_key_press
        input_layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.send_button.setMaximumWidth(80)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # === Status Bar ===
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 8))
        self.status_label.setStyleSheet("color: #888;")
        main_layout.addWidget(self.status_label)
        
        # Display initial chat
        self.display_buddy_message(f"{get_greeting()}\n\nI'm your AI buddy! Feel free to chat with me about anything. 😊")
    
    def setup_timers(self):
        """Setup update timers"""
        
        # Update time every minute
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(60000)  # Every minute
        
        # Update weather every 10 minutes
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(config.UPDATE_WEATHER_INTERVAL)
        
        # Update emotion every 5 seconds
        self.emotion_timer = QTimer()
        self.emotion_timer.timeout.connect(self.update_emotion_display)
        self.emotion_timer.start(5000)
    
    def handle_input_key_press(self, event):
        """Handle key press in input field"""
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.send_message()
        else:
            QTextEdit.keyPressEvent(self.input_field, event)
    
    def send_message(self):
        """Send user message to AI"""
        message = self.input_field.toPlainText().strip()
        
        if not message:
            return
        
        # Display user message
        self.display_user_message(message)
        self.input_field.clear()
        
        # Update status
        self.status_label.setText("Buddy is thinking...")
        self.send_button.setEnabled(False)
        
        # Detect emotion from user input
        emotion = self.emotion_manager.detect_emotion_from_message(message)
        self.emotion_manager.set_emotion(emotion)
        
        # Send to AI in background thread
        self.ai_worker = AIResponseWorker(
            self.ai_buddy,
            message,
            config.SYSTEM_PROMPT
        )
        self.ai_worker.response_ready.connect(self.on_ai_response)
        self.ai_worker.error_occurred.connect(self.on_ai_error)
        self.ai_worker.start()
    
    def on_ai_response(self, response: str):
        """Handle AI response"""
        # Detect emotion from response
        emotion = self.emotion_manager.detect_emotion_from_response(response)
        self.emotion_manager.set_emotion(emotion)
        
        # Display response
        self.display_buddy_message(response)
        
        # Update status
        self.status_label.setText("Ready")
        self.send_button.setEnabled(True)
        
        # Log message
        from utils import log_message
        log_message(f"Chat - User message received")
        log_message(f"Chat - Buddy response sent")
    
    def on_ai_error(self, error: str):
        """Handle AI error"""
        self.display_buddy_message(f"❌ {error}")
        self.status_label.setText("Error")
        self.send_button.setEnabled(True)
    
    def display_user_message(self, message: str):
        """Display user message in chat"""
        self.chat_display.append(f"\n👤 You:\n{message}\n")
    
    def display_buddy_message(self, message: str):
        """Display buddy message in chat"""
        emoji = self.emotion_manager.get_emotion_emoji()
        self.chat_display.append(f"\n{emoji} Buddy:\n{message}\n")
    
    def update_time(self):
        """Update time display"""
        self.time_label.setText(get_current_time())
    
    def update_weather(self):
        """Update weather display"""
        weather = self.weather_manager.get_weather()
        if weather:
            weather_text = self.weather_manager.format_weather_string()
            self.weather_label.setText(weather_text)
        else:
            self.weather_label.setText("🌤️ Weather unavailable")
    
    def update_emotion_display(self):
        """Update emotion emoji display"""
        emoji = self.emotion_manager.get_emotion_emoji()
        self.buddy_label.setText(f"{config.BUDDY_NAME} {emoji}")
    
    def get_stylesheet(self) -> str:
        """Get application stylesheet"""
        return """
        QMainWindow {
            background-color: #ffffff;
        }
        QTextEdit {
            font-family: Arial;
            font-size: 10px;
        }
        QPushButton {
            font-family: Arial;
        }
        """
    
    def closeEvent(self, event):
        """Handle application close"""
        from utils import log_message
        log_message("Application closed")
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Check if Ollama is available
    buddy = AIBuddy(config.AI_MODEL)
    if not buddy.is_connected:
        print("⚠️ Warning: Ollama is not running!")
        print("Please start Ollama to use the AI features.")
        print("Download Ollama from: https://ollama.ai")
    
    # Create and show main window
    window = DesktopAIBuddy()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
