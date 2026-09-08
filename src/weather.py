"""
Weather integration for Desktop AI Buddy
Uses Open-Meteo free weather API (no API key needed)
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional

class WeatherManager:
    """Manages weather data and updates"""
    
    # Open-Meteo API (free, no authentication needed)
    GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, location: str = "New York", timeout: int = 10):
        """
        Initialize weather manager
        
        Args:
            location: City name or location string
            timeout: Request timeout in seconds
        """
        self.location = location
        self.timeout = timeout
        self.current_weather = None
        self.latitude = None
        self.longitude = None
    
    def get_coordinates(self, location: str) -> Optional[tuple]:
        """
        Get latitude and longitude for a location
        
        Args:
            location: City name or location string
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        try:
            params = {
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            response = requests.get(
                self.GEOCODING_API,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                self.latitude = result["latitude"]
                self.longitude = result["longitude"]
                return (self.latitude, self.longitude)
            
            return None
            
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None
    
    def get_weather(self, location: Optional[str] = None) -> Optional[Dict]:
        """
        Get current weather for a location
        
        Args:
            location: City name or location string. Uses self.location if not provided
            
        Returns:
            Dictionary with weather data or None if error
        """
        if location:
            self.location = location
        
        try:
            # Get coordinates
            coords = self.get_coordinates(self.location)
            if not coords:
                return None
            
            latitude, longitude = coords
            
            # Get weather
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
                "temperature_unit": "celsius",
                "timezone": "auto"
            }
            
            response = requests.get(
                self.WEATHER_API,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("current"):
                current = data["current"]
                self.current_weather = {
                    "location": self.location,
                    "temperature": current.get("temperature_2m"),
                    "weather_code": current.get("weather_code"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "humidity": current.get("relative_humidity_2m"),
                    "time": current.get("time"),
                    "description": self._get_weather_description(current.get("weather_code"))
                }
                
                return self.current_weather
            
            return None
            
        except Exception as e:
            print(f"Error getting weather: {e}")
            return None
    
    @staticmethod
    def _get_weather_description(code: int) -> str:
        """
        Convert WMO weather code to description
        
        Args:
            code: WMO weather code
            
        Returns:
            Human-readable weather description
        """
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy with rime",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return descriptions.get(code, "Unknown")
    
    def format_weather_string(self) -> str:
        """
        Format weather data as a readable string
        
        Returns:
            Formatted weather string
        """
        if not self.current_weather:
            return "Weather data not available"
        
        w = self.current_weather
        return (
            f"🌍 {w['location']}\n"
            f"🌡️ {w['temperature']}°C\n"
            f"☁️ {w['description']}\n"
            f"💨 Wind: {w['wind_speed']} km/h\n"
            f"💧 Humidity: {w['humidity']}%"
        )
    
    def get_weather_emoji(self) -> str:
        """
        Get emoji based on current weather
        
        Returns:
            Weather emoji
        """
        if not self.current_weather:
            return "🌤️"
        
        code = self.current_weather.get("weather_code", 0)
        
        if code == 0:
            return "☀️"  # Clear sky
        elif code == 2:
            return "⛅"  # Partly cloudy
        elif code == 3:
            return "☁️"  # Overcast
        elif code in [45, 48]:
            return "🌫️"  # Fog
        elif code in [51, 53, 55, 61, 63, 65]:
            return "🌧️"  # Rain
        elif code in [71, 73, 75, 77]:
            return "❄️"  # Snow
        elif code in [80, 81, 82]:
            return "🌧️"  # Rain showers
        elif code in [95, 96, 99]:
            return "⛈️"  # Thunderstorm
        
        return "🌤️"  # Default
