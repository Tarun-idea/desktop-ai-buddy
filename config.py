# Desktop AI Buddy Configuration

# AI Model Settings
AI_MODEL = "mistral"  # Options: mistral, llama2, neural-chat, dolphin-mixtral
OLLAMA_HOST = "http://localhost:11434"  # Ollama server address
OLLAMA_TIMEOUT = 30  # Timeout in seconds

# Buddy Settings
BUDDY_NAME = "DESK-Buddy"
BUDDY_WIDTH = 400
BUDDY_HEIGHT = 500
WINDOW_TITLE = "DESK-Buddy - Your AI Companion"

# Weather Settings
WEATHER_ENABLED = True
LOCATION = "New York"  # Default location
WEATHER_API = "open-meteo"  # Using free Open-Meteo API
UPDATE_WEATHER_INTERVAL = 600000  # Update every 10 minutes (in milliseconds)

# Chat Settings
MAX_MESSAGE_LENGTH = 500
CHAT_HISTORY_LIMIT = 50
AUTO_SCROLL_CHAT = True

# UI Settings
THEME = "dark"  # Options: dark, light
FONT_SIZE = 11
BUDDY_EMOTION_DISPLAY_TIME = 3000  # Show emotion for 3 seconds (in milliseconds)

# Emotions
EMOTIONS = {
    "happy": "😊",
    "sad": "😢",
    "thinking": "🤔",
    "excited": "🤩",
    "confused": "😕",
    "neutral": "😶"
}

# System Prompt for AI
SYSTEM_PROMPT = """You are DESK-Buddy, a friendly and helpful desktop AI companion. 
You are warm, conversational, and always ready to help with questions, creative tasks, or just chat.
Keep responses concise and friendly (2-3 sentences max).
Show personality and emotions in your responses."""

# Enable/Disable Features
ENABLE_VOICE_OUTPUT = False  # Text-to-speech (requires additional setup)
ENABLE_VOICE_INPUT = False   # Speech recognition (requires additional setup)
ENABLE_NOTIFICATIONS = True  # Desktop notifications

# Logging
DEBUG_MODE = True
LOG_FILE = "logs/buddy.log"