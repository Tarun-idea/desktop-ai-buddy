"""
Utility functions for Desktop AI Buddy
"""

from datetime import datetime
import os
import sys

def get_current_time() -> str:
    """Get current time in readable format"""
    return datetime.now().strftime("%I:%M %p")

def get_current_time_12h() -> str:
    """Get current time in 12-hour format"""
    return datetime.now().strftime("%I:%M %p")

def get_current_time_24h() -> str:
    """Get current time in 24-hour format"""
    return datetime.now().strftime("%H:%M")

def get_greeting() -> str:
    """Get appropriate greeting based on time of day"""
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning! ☀️"
    elif 12 <= hour < 17:
        return "Good afternoon! 🌤️"
    elif 17 <= hour < 21:
        return "Good evening! 🌅"
    else:
        return "Good night! 🌙"

def get_day_of_week() -> str:
    """Get current day of week"""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[datetime.now().weekday()]

def get_full_date() -> str:
    """Get full date string"""
    return datetime.now().strftime("%A, %B %d, %Y")

def ensure_dir_exists(directory: str):
    """Ensure a directory exists, create if not"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text

def is_valid_location(location: str) -> bool:
    """Check if location string is valid"""
    return len(location.strip()) > 0 and len(location) < 100

def format_response(response: str) -> str:
    """Format AI response for display"""
    # Remove extra whitespace
    response = " ".join(response.split())
    return response

def get_app_version() -> str:
    """Get application version"""
    return "1.0.0"

def get_resource_path(resource: str) -> str:
    """Get path to resource file"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, "assets", resource)

def log_message(message: str, log_file: str = "logs/buddy.log"):
    """Log message to file"""
    ensure_dir_exists(os.path.dirname(log_file))
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_system_info() -> dict:
    """Get system information"""
    return {
        "platform": sys.platform,
        "python_version": sys.version,
        "timestamp": get_full_date()
    }
