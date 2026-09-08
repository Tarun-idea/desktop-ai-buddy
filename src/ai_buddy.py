"""
AI Buddy - LLM Integration
Handles communication with local Ollama models
"""

import requests
import json
import sys
from typing import Optional, Iterator
from datetime import datetime

class AIBuddy:
    """AI Buddy powered by local Ollama models"""
    
    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434", timeout: int = 30):
        """
        Initialize AI Buddy
        
        Args:
            model: Model name (e.g., 'mistral', 'llama2', 'neural-chat')
            host: Ollama server address
            timeout: Request timeout in seconds
        """
        self.model = model
        self.host = host
        self.timeout = timeout
        self.conversation_history = []
        self.is_connected = False
        
        # Check connection
        self.check_connection()
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            self.is_connected = response.status_code == 200
            return self.is_connected
        except Exception as e:
            print(f"Connection error: {e}")
            self.is_connected = False
            return False
    
    def is_model_available(self) -> bool:
        """Check if the configured model is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                for model_info in models:
                    if model_info.get("name", "").startswith(self.model):
                        return True
            return False
        except Exception as e:
            print(f"Error checking model availability: {e}")
            return False
    
    def chat(self, message: str, system_prompt: str = None) -> Optional[str]:
        """Send a message and get AI response"""
        if not self.is_connected:
            return "❌ Error: Ollama is not running. Please start Ollama first!"
        
        try:
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": message})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": 200,
                    "temperature": 0.7
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_message = data.get("message", {}).get("content", "")
                
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                return assistant_message
            else:
                return f"❌ Error: {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "❌ Error: Request timed out. Ollama might be slow to respond."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_available_models(self) -> list:
        """Get list of available models from Ollama"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model_info in data.get("models", []):
                    models.append(model_info.get("name", ""))
                return models
            return []
        except Exception as e:
            print(f"Error getting models: {e}")
            return []
    
    def set_model(self, model: str):
        """Change AI model"""
        self.model = model
        self.clear_history()
