#!/usr/bin/env python3
"""
Tomorrow's Weather SMS Script (GitHub Version)
Gets tomorrow's weather forecast for zip code 10977 and sends it via SMS.
Uses environment variables for API keys for security.
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

# Configuration
ZIP_CODE = "10977"
PHONE_NUMBERS = [
    "+18453216547",  # Replace with your actual phone numbers
    "+18451234567",  # Add more numbers as needed
]

def get_coordinates_from_zip(zip_code, api_key):
    """Get latitude and longitude from zip code using Geocoding API."""
    geocoding_url = "http://api.openweathermap.org/geo/1.0/zip"
    params = {
        'zip': f"{zip_code},US",
        'appid': api_key
    }
    
    try:
        response = requests.get(geocoding_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'lat': data['lat'],
            'lon': data['lon'],
            'name': data['name']
        }
        
    except requests.RequestException as e:
        raise Exception(f"Error getting coordinates: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected geocoding data format: {e}")

def get_tomorrow_weather(zip_code):
    """Get tomorrow's weather forecast using One Call API 3.0."""
    # Get OpenWeatherMap API key from environment variable
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")
    
    try:
        # First, get coordinates from zip code
        location_info = get_coordinates_from_zip(zip_code, api_key)
        
        # Use One Call API 3.0 - include daily forecast
        onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            'lat': location_info['lat'],
            'lon': location_info['lon'],
            'exclude': 'minutely,hourly,alerts',  # Get current and daily
            'appid': api_key,
            'units': 'imperial'  # For Fahrenheit
        }
        
        response = requests.get(onecall_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract tomorrow's weather information (daily[1] is tomorrow)
        tomorrow = data['daily'][1]
        
        # Calculate tomorrow's date
        tomorrow_date = datetime.now() + timedelta(days=1)
        
        weather_info = {
            'location': location_info['name'],
            'date': tomorrow_date.strftime("%A, %B %d"),
            'high_temp': round(tomorrow['temp']['max']),
            'low_temp': round(tomorrow['temp']['min']),
            'morning_temp': round(tomorrow['temp']['morn']),
            'day_temp': round(tomorrow['temp']['day']),
            'evening_temp': round(tomorrow['temp']['eve']),
            'night_temp': round(tomorrow['temp']['night']),
            'humidity': tomorrow['humidity'],
            'description': tomorrow['weather'][0]['description'].title(),
            'wind_speed': tomorrow['wind_speed'],
            'pop': round(tomorrow['pop'] * 100),  # Probability of precipitation
            'uv_index': round(tomorrow['uvi'])
        }
        
        return weather_info
        
    except requests.RequestException as e:
        raise Exception(f"Error fetching weather data: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected weather data format: {e}")

def format_tomorrow_weather_message(weather_info):
    """Format tomorrow's weather information into a readable SMS message with emojis."""
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Add precipitation info if there's a chance of rain
    precipitation_text = ""
    if weather_info['pop'] > 0:
        precipitation_text = f"🌧️ Rain chance: {weather_info['pop']}%\n"
    
    # Add UV index warning if high
    uv_text = ""
    if weather_info['uv_index'] >= 6:
        uv_text = f"☀️ UV Index: {weather_info['uv_index']} (High - use sunscreen)\n"
    elif weather_info['uv_index'] >= 3:
        uv_text = f"☀️ UV Index: {weather_info['uv_index']} (Moderate)\n"
    
    # SMS message WITH emojis (this is what recipients will see)
    message = f"""🌤️ Tomorrow's Weather for {weather_info['location']}
📅 {weather_info['date']}
🕙 Forecast sent: {current_time}

🌡️ High: {weather_info['high_temp']}°F | Low: {weather_info['low_temp']}°F
📝 Conditions: {weather_info['description']}
💧 Humidity: {weather_info['humidity']}%
💨 Wind: {weather_info['wind_speed']} mph
{precipitation_text}{uv_text}
🌅 Morning: {weather_info['morning_temp']}°F
☀️ Afternoon: {weather_info['day_temp']}°F
🌆 Evening: {weather_info['evening_temp']}°F
🌙 Night: {weather_info['night_temp']}°F

Have a great day tomorrow! 🌟"""
    
    return message

def send_sms(message, phone_numbers):
    """Send SMS using Twilio API."""
    # Get Twilio credentials from environment variables
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER')
    
    if not all([account_sid, auth_token, from_number]):
        raise ValueError("Twilio credentials not set. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER environment variables.")
    
    client = Client(account_sid, auth_token)
    
    results = []
    for phone_number in phone_numbers:
        try:
            # Create message using from phone number
            message_obj = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )
            
            results.append({
                'number': phone_number,
                'status': 'sent',
                'sid': message_obj.sid
            })
            print(f"SMS sent successfully to {phone_number}")
            
        except Exception as e:
            results.append({
                'number': phone_number,
                'status': 'failed',
                'error': str(e)
            })
            print(f"Failed to send SMS to {phone_number}: {e}")
    
    return results

def main():
    """Main function to orchestrate weather fetching and SMS sending."""
    try:
        print("Fetching tomorrow's weather forecast...")
        weather_info = get_tomorrow_weather(ZIP_CODE)
        
        print(f"Tomorrow's weather for {weather_info['location']}: {weather_info['high_temp']}F/{weather_info['low_temp']}F, {weather_info['description']}")
        
        print("Formatting message...")
        message = format_tomorrow_weather_message(weather_info)
        
        print("Sending SMS messages...")
        results = send_sms(message, PHONE_NUMBERS)
        
        # Summary
        successful = sum(1 for r in results if r['status'] == 'sent')
        failed = sum(1 for r in results if r['status'] == 'failed')
        
        print(f"Summary: {successful} sent, {failed} failed")
        
        if failed > 0:
            print("Failed messages:")
            for result in results:
                if result['status'] == 'failed':
                    print(f"  - {result['number']}: {result['error']}")
        
        # Log the run
        log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Weather SMS sent to {successful} numbers"
        print(log_message)
        
    except Exception as e:
        print(f"Error: {e}")
        # Log the error
        error_log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e}"
        print(error_log)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
