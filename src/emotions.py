"""
Emotion management for Desktop AI Buddy
Handles emotional states and responses based on chat context
"""

import random
from enum import Enum

class Emotion(Enum):
    """Available emotions for the buddy"""
    HAPPY = "😊"
    SAD = "😢"
    THINKING = "🤔"
    EXCITED = "🤩"
    CONFUSED = "😕"
    NEUTRAL = "😶"
    COOL = "😎"
    LOVING = "🥰"


class EmotionManager:
    """Manages buddy emotions based on conversation context"""
    
    def __init__(self):
        self.current_emotion = Emotion.NEUTRAL
        self.emotion_history = []
    
    def detect_emotion_from_message(self, message: str) -> Emotion:
        """
        Detect emotion based on user's message
        
        Args:
            message: User's input message
            
        Returns:
            Emotion enum value
        """
        message_lower = message.lower()
        
        # Happy triggers
        if any(word in message_lower for word in ["hello", "hi", "hey", "thanks", "great", "awesome", "good"]):
            return Emotion.HAPPY
        
        # Sad triggers
        if any(word in message_lower for word in ["sad", "bad", "angry", "frustrated", "upset", "hate"]):
            return Emotion.SAD
        
        # Thinking triggers
        if any(word in message_lower for word in ["how", "what", "why", "explain", "help", "teach"]):
            return Emotion.THINKING
        
        # Excited triggers
        if any(word in message_lower for word in ["wow", "amazing", "incredible", "love", "yes!", "excited"]):
            return Emotion.EXCITED
        
        # Confused triggers
        if any(word in message_lower for word in ["?", "confused", "what", "huh", "unclear", "weird"]):
            return Emotion.CONFUSED
        
        # Default to neutral
        return Emotion.NEUTRAL
    
    def detect_emotion_from_response(self, response: str) -> Emotion:
        """
        Detect emotion based on AI's response
        
        Args:
            response: AI's generated response
            
        Returns:
            Emotion enum value
        """
        response_lower = response.lower()
        
        # Happy responses
        if any(word in response_lower for word in ["happy", "great", "wonderful", "excited", "love"]):
            return Emotion.HAPPY
        
        # Thinking responses
        if any(word in response_lower for word in ["let me think", "interesting", "hmm", "consider"]):
            return Emotion.THINKING
        
        # Loving responses
        if any(word in response_lower for word in ["love", "caring", "help you", "support"]):
            return Emotion.LOVING
        
        # Cool responses
        if any(word in response_lower for word in ["cool", "awesome", "amazing", "incredible"]):
            return Emotion.COOL
        
        return Emotion.NEUTRAL
    
    def set_emotion(self, emotion: Emotion):
        """Set current emotion"""
        self.current_emotion = emotion
        self.emotion_history.append(emotion)
    
    def get_current_emotion(self) -> Emotion:
        """Get current emotion"""
        return self.current_emotion
    
    def get_random_emotion(self) -> Emotion:
        """Get a random emotion for idle state"""
        return random.choice(list(Emotion))
    
    def reset_emotion(self):
        """Reset to neutral emotion"""
        self.current_emotion = Emotion.NEUTRAL
    
    def get_emotion_emoji(self) -> str:
        """Get emoji for current emotion"""
        return self.current_emotion.value


# Emotion-based response modifiers
EMOTION_PREFIXES = {
    Emotion.HAPPY: ["😊 ", ""],
    Emotion.SAD: ["😢 ", "Hmm, "],
    Emotion.THINKING: ["🤔 Interesting... ", "Let me think... "],
    Emotion.EXCITED: ["🤩 ", "Wow! "],
    Emotion.CONFUSED: ["😕 ", "Hmm, I'm not sure about that. "],
    Emotion.NEUTRAL: [""],
    Emotion.COOL: ["😎 ", "Nice! "],
    Emotion.LOVING: ["🥰 ", "I love helping! "],
}