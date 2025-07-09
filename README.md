# 🌤️ Weather SMS Automation

Automated daily weather forecast SMS system that sends tomorrow's weather with beautiful emojis to multiple phone numbers.

## 📱 Features

- **Tomorrow's Weather Forecast**: Get detailed weather for the next day
- **Beautiful Emojis**: Rich SMS messages with weather icons
- **Multiple Recipients**: Send to multiple phone numbers at once
- **Detailed Information**: High/Low temps, conditions, UV index, rain probability
- **Automated Scheduling**: Set up daily runs at any time
- **Multiple Deployment Options**: Local scheduling or cloud deployment

## 🚀 Sample SMS Output

```
🌤️ Tomorrow's Weather for Spring Valley
📅 Thursday, July 10
🕙 Forecast sent: July 9, 2025 at 10:00 PM

🌡️ High: 82°F | Low: 71°F
📝 Conditions: Moderate Rain
💧 Humidity: 78%
💨 Wind: 6.2 mph
🌧️ Rain chance: 85%
☀️ UV Index: 6 (High - use sunscreen)

🌅 Morning: 73°F
☀️ Afternoon: 82°F
🌆 Evening: 78°F
🌙 Night: 71°F

Have a great day tomorrow! 🌟
```

## 🛠️ Setup

### Prerequisites

- Python 3.7+
- OpenWeatherMap API key (free)
- Twilio account (free tier available)

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
   export TWILIO_ACCOUNT_SID="your_twilio_account_sid"
   export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
   export TWILIO_FROM_NUMBER="your_twilio_phone_number"
   ```

4. **Update configuration**
   
   Edit `weather_sms_github.py` to set your zip code and phone numbers:
   ```python
   ZIP_CODE = "10977"  # Your zip code
   PHONE_NUMBERS = [
       "+1234567890",  # Your phone numbers
       "+0987654321",
   ]
   ```

## 🔑 Getting API Keys

### OpenWeatherMap
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Set `OPENWEATHER_API_KEY` environment variable

### Twilio
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number
4. Set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_FROM_NUMBER`

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
2. **API key errors**: Verify keys are set correctly
3. **SMS delivery issues**: Check Twilio account balance and phone number verification
4. **Weather data errors**: Verify OpenWeatherMap API key and zip code

### Debugging

Run with detailed error output:
```bash
python weather_sms_github.py 2>&1 | tee debug.log
```

## 📊 Monitoring

- Check logs for execution status
- Monitor Twilio console for SMS delivery
- Set up alerts for failed executions (cloud deployments)

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
