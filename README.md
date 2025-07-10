# 🌤️ Weather SMS Automation with AI Rain Analysis

Automated daily weather forecast SMS system that sends tomorrow's weather with AI-powered rain analysis and beautiful emojis to multiple phone numbers.

## 📱 Features

- **Tomorrow's Weather Forecast**: Get detailed weather for the next day
- **AI-Powered Rain Analysis**: OpenAI GPT-4 analyzes hourly rain data for precise timing
- **Beautiful Emojis**: Rich SMS messages with weather icons
- **Multiple Recipients**: Send to multiple phone numbers at once
- **Detailed Information**: High/Low temps, conditions, UV index, rain probability
- **Enhanced SMS Delivery**: Individual message sending to overcome Twilio trial limitations
- **Automated Scheduling**: Set up daily runs at any time
- **Multiple Deployment Options**: Local scheduling or cloud deployment
- **Secure Configuration**: Environment variables for all API keys

## 🚀 Sample SMS Output

```
🌤️ Tomorrow's Weather for Spring Valley
📅 Thursday, July 11
🕙 Forecast sent: July 10, 2025 at 05:01 PM

🌡️ High: 91°F | Low: 69°F
📝 Conditions: Scattered Clouds
💧 Humidity: 68%
💨 Wind: 8.2 mph
🌧️ Rain chance: 15%
🌦️ Rain Forecast: Light rain expected from 3 PM until 4 PM.

🌅 Morning: 73°F
☀️ Afternoon: 89°F
🌆 Evening: 85°F
🌙 Night: 72°F

Have a great day tomorrow! 🌟
```

## 🛠️ Setup

### Prerequisites

- Python 3.7+
- OpenWeatherMap API key (free)
- Twilio account (free tier available)
- OpenAI API key (for AI rain analysis)
- Python packages: `requests`, `twilio`, `openai`, `httpx`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/weather-forecast-sms.git
   cd weather-forecast-sms
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file or set environment variables:
   ```bash
   export OPENWEATHER_API_KEY="your_openweather_api_key"
   export OPENAI_API_KEY="your_openai_api_key"
   export TWILIO_ACCOUNT_SID="your_twilio_account_sid"
   export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
   export TWILIO_FROM_NUMBER="your_twilio_phone_number"
   ```

4. **Update configuration**
   
   Edit `weather_sms_github.py` to set your zip code and phone numbers:
   ```python
   ZIP_CODE = "YOUR_ZIP_CODE"  # Replace with your zip code
   PHONE_NUMBERS = [
       "+1234567890",  # Replace with your actual phone numbers
       "+0987654321",  # Add more numbers as needed
   ]
   ```

## 🔑 Getting API Keys

### OpenWeatherMap
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Set `OPENWEATHER_API_KEY` environment variable

### OpenAI (for AI Rain Analysis)
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Get your API key
3. Set `OPENAI_API_KEY` environment variable
4. Note: Requires credits for API usage

### Twilio
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number
4. **Important**: Verify all recipient phone numbers in Twilio Console (trial accounts)
5. Set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_FROM_NUMBER`

## 🏃‍♂️ Running

### Manual Run
```bash
python weather_sms_github.py
```

### Scheduled Runs

#### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set to run daily at your preferred time
4. Set action to run: `python path/to/weather_sms_github.py`

#### Linux/Mac Cron
```bash
# Run daily at 10 PM
0 22 * * * cd /path/to/weather-forecast-sms && python weather_sms_github.py
```

## ☁️ Cloud Deployment

### GitHub Actions (Recommended)
1. Fork this repository
2. Add secrets in GitHub repository settings:
   - `OPENWEATHER_API_KEY`
   - `OPENAI_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_FROM_NUMBER`
3. Enable Actions in your repository

### Other Cloud Options
- **PythonAnywhere**: Free tier with scheduled tasks
- **Render**: Free tier with cron jobs
- **Railway**: Monthly credits with cron support

See `SCHEDULING_GUIDE.md` for detailed cloud deployment instructions.

## 📁 File Structure

```
weather-forecast-sms/
├── weather_sms_github.py      # Main script with environment variables
├── requirements.txt           # Python dependencies
├── SCHEDULING_GUIDE.md       # Detailed deployment guide
├── .gitignore                # Git ignore file
├── README.md                 # This file
└── .github/
    └── workflows/
        └── weather-sms.yml   # GitHub Actions workflow
```

## 🔧 Configuration

### Customization Options

- **ZIP_CODE**: Change the location for weather data
- **PHONE_NUMBERS**: Add/remove recipient phone numbers
- **Message Format**: Customize the SMS message template
- **Weather Data**: Add/remove weather information fields

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `OPENAI_API_KEY` | OpenAI API key for rain analysis | Yes |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | Yes |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | Yes |
| `TWILIO_FROM_NUMBER` | Twilio phone number | Yes |

## 🚨 Security Notes

- **Never commit API keys** to version control
- Use environment variables for all sensitive data
- The `.gitignore` file excludes credential files
- For cloud deployment, use secrets management

## 🐛 Troubleshooting

### Common Issues

1. **Unicode/Emoji errors**: Ensure your environment supports UTF-8
2. **API key errors**: Verify all keys are set correctly (OpenWeather, OpenAI, Twilio)
3. **SMS delivery issues**: 
   - Check Twilio account balance and phone number verification
   - **Trial accounts**: Verify ALL recipient phone numbers in Twilio Console
   - Multiple recipients: Script sends individually to overcome trial limitations
4. **Weather data errors**: Verify OpenWeatherMap API key and zip code
5. **AI rain analysis errors**: Check OpenAI API key and account credits
6. **SSL/Network errors**: Script includes SSL bypass for corporate networks

### Debugging

Run with detailed error output:
```bash
python weather_sms_github.py 2>&1 | tee debug.log
```

## 📊 Monitoring

- Check logs for execution status
- Monitor Twilio console for SMS delivery
- Set up alerts for failed executions (cloud deployments)

## ✨ New Features

### AI Rain Analysis
- **Powered by OpenAI GPT-4**: Analyzes hourly rain data for precise timing
- **Smart Summaries**: "Light rain expected from 3 PM until 4 PM"
- **SMS Integration**: Rain forecasts included in weather messages
- **Error Handling**: Graceful fallback if AI analysis fails

### Enhanced SMS Delivery
- **Individual Message Sending**: Overcomes Twilio trial account batch limitations
- **Delivery Delays**: 2-second delays between messages to prevent rate limiting
- **Separate Client Instances**: Each message gets its own Twilio client
- **Enhanced Logging**: Detailed status reporting for each message

### Security Improvements
- **Environment Variables**: All sensitive data moved to environment variables
- **GitHub Security**: Automatic secret detection and blocking
- **Clean Repository**: Test files and credentials excluded from version control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [Twilio](https://www.twilio.com/) for SMS services
- Weather icons and emojis for beautiful formatting

---

**Happy Weather Forecasting!** 🌤️📱
