from .base_agent import BaseAgent
import requests
import os

class WeatherAgent(BaseAgent):
    def get_agent_name(self):
        return "Weather Agent"
    
    def should_handle(self, message: str) -> bool:
        weather_keywords = [
            'weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy',
            'humidity', 'wind', 'speed', 'climate', 'meteorology', 'storm',
            'snow', 'fog', 'mist', 'drizzle', 'thunderstorm', 'hurricane',
            'typhoon', 'cyclone', 'barometer', 'pressure', 'uv', 'index',
            'dew point', 'visibility', 'precipitation', 'chance of rain'
        ]
        return any(keyword in message.lower() for keyword in weather_keywords)
    
    def handle_message(self, message: str, context: dict = None) -> str:
        location = self.extract_location(message)
        if not location:
            return "Please specify a location for weather information. Example: 'weather in London' or 'temperature in Tokyo'"
        
        weather_data = self.get_weather_data(location)
        if weather_data:
            return self.format_weather_response(weather_data, location)
        else:
            return f"Could not fetch weather data for {location}. Please check if the city name is correct."
    
    def extract_location(self, message: str) -> str:
        message_lower = message.lower()
        
        # Common patterns for location extraction
        patterns = [
            r'weather in (\w+)',
            r'temperature in (\w+)', 
            r'forecast for (\w+)',
            r'humidity in (\w+)',
            r'wind speed in (\w+)'
        ]
        
        import re
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                return match.group(1).title()
        
        # Fallback: look for city names after weather keywords
        words = message_lower.split()
        for i, word in enumerate(words):
            if word in ['in', 'at', 'for', 'of'] and i + 1 < len(words):
                return words[i + 1].title()
        
        return None
    
    def get_weather_data(self, location: str):
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            return None
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Weather API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Weather API exception: {e}")
            return None
    
    def format_weather_response(self, data: dict, location: str) -> str:
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        
        return f"""Weather in {location}:
• Temperature: {temp}°C
• Conditions: {desc.title()}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} m/s
• Pressure: {pressure} hPa"""