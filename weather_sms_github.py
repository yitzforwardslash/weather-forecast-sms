#!/usr/bin/env python3
"""
Tomorrow's Weather SMS Script (GitHub Version)
Gets tomorrow's weather forecast for zip code 10977 and sends it via SMS.
Uses environment variables for API keys for security.
"""
import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from openai import OpenAI

# Configuration
ZIP_CODE = "YOUR_ZIP_CODE"  # Replace with your zip code
PHONE_NUMBERS = [
    "+1234567890",  # Replace with your actual phone numbers
    "+0987654321"   # Add more numbers as needed
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
        
        # Use One Call API 3.0 - include daily and hourly forecast
        onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            'lat': location_info['lat'],
            'lon': location_info['lon'],
            'exclude': 'minutely,alerts',  # Get current, daily, and hourly
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
        tomorrow_start = tomorrow_date.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_end = tomorrow_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Extract hourly data for tomorrow only
        tomorrow_hourly = []
        for hour_data in data['hourly']:
            hour_time = datetime.fromtimestamp(hour_data['dt'])
            if tomorrow_start <= hour_time <= tomorrow_end:
                tomorrow_hourly.append({
                    'time': hour_time,
                    'pop': hour_data.get('pop', 0) * 100,  # Probability of precipitation
                    'rain': hour_data.get('rain', {}).get('1h', 0),  # Rain in mm
                    'weather': hour_data['weather'][0]['main']
                })
        
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
            'uv_index': round(tomorrow['uvi']),
            'hourly_rain': tomorrow_hourly  # Hourly rain data for AI analysis
        }
        
        return weather_info
        
    except requests.RequestException as e:
        raise Exception(f"Error fetching weather data: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected weather data format: {e}")


def analyze_rain_forecast(hourly_rain):
    """Use OpenAI to get a concise summary of the rain forecast from hourly data."""
    import os
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Create HTTP client that bypasses SSL verification
    import httpx
    http_client = httpx.Client(verify=False)
    openai_client = OpenAI(api_key=openai_api_key, http_client=http_client)

    # Prepare data string for OpenAI prompt
    rain_data = "".join(
        f"{entry['time'].strftime('%I:%M %p')}: Rain: {entry['rain']}mm - Chance: {entry['pop']}%\n"
        for entry in hourly_rain if entry['rain'] > 0
    )

    if not rain_data:
        return ""  # No rain expected

    # Compose prompt
    prompt = (
        "You are a weather analyst. Given the hourly rain data, produce a short forecast describing "
        "the expected rain periods. Just the rain times in short, 'always indicating when it will start until when it will end' (e.g. Light rain expected from 10 AM until 11:30 AM and heavy rain after 8 PM until the end of the day). This will be used for SMS notifications"
        "Please summarize the rain situation concisely."
    )

    # Call OpenAI to generate the summary
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": rain_data}
            ],
            max_tokens=200
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        raise Exception(f"Error during AI analysis: {e}")

def format_tomorrow_weather_message(weather_info):
    """Format tomorrow's weather information into a readable SMS message with emojis."""
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Add precipitation info if there's a chance of rain
    precipitation_text = ""
    if weather_info['pop'] > 0:
        precipitation_text = f"🌧️ Rain chance: {weather_info['pop']}%\n"
    
    # Add AI rain summary if available
    rain_summary_text = ""
    if weather_info.get('rain_summary'):
        rain_summary_text = f"🌦️ Rain Forecast: {weather_info['rain_summary']}\n"
    
    # SMS message WITH emojis (this is what recipients will see)
    message = f"""🌤️ Tomorrow's Weather for {weather_info['location']}
📅 {weather_info['date']}
🕙 Forecast sent: {current_time}

🌡️ High: {weather_info['high_temp']}°F | Low: {weather_info['low_temp']}°F
📝 Conditions: {weather_info['description']}
💧 Humidity: {weather_info['humidity']}%
💨 Wind: {weather_info['wind_speed']} mph
{precipitation_text}{rain_summary_text}
🌅 Morning: {weather_info['morning_temp']}°F
☀️ Afternoon: {weather_info['day_temp']}°F
🌆 Evening: {weather_info['evening_temp']}°F
🌙 Night: {weather_info['night_temp']}°F

Have a great day tomorrow! 🌟"""
    
    return message

def send_sms(message, phone_numbers):
    """Send SMS using Twilio API."""
    # Get Twilio credentials from environment variables
    import os
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
        
        # Generate AI rain analysis if there's rain data
        rain_summary = ""
        if weather_info['hourly_rain']:
            print("Analyzing rain forecast with AI...")
            try:
                rain_summary = analyze_rain_forecast(weather_info['hourly_rain'])
                if rain_summary:
                    print(f"AI Rain Analysis: {rain_summary}")
            except Exception as e:
                print(f"Warning: Could not generate AI rain analysis: {e}")
        
        weather_info['rain_summary'] = rain_summary
        
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