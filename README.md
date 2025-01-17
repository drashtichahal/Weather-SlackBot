# Weather SlackBot 🌦️

A simple Slackbot that provides live weather updates in response to user queries like **"How is the weather?"**. The bot fetches real-time weather data using the OpenWeatherMap API and responds directly in your Slack workspace.

---

## Features ✨
- **Live Weather Data:** Fetches current weather conditions including temperature, humidity, and general weather descriptions.
- **Location Support:** Users can specify locations, e.g., **"How is the weather in Paris?"**, or default to a pre-configured location.
- **Error Handling:** Responds gracefully to errors, such as invalid queries or API failures.
- **Interactive Slack Integration:** Seamlessly interacts with Slack channels and direct messages.

---

## Setup Instructions 🛠️

### Prerequisites
- Python 3.9+
- Slack workspace with admin permissions to register a bot
- API keys for:
  - [OpenWeatherMap API](https://openweathermap.org/api)
  - Slack Bot Token (from Slack API)

---

### Installation Steps

1. **Clone the Repository**  
   Open your terminal and run:
   ```bash
   git clone https://github.com/yourusername/Weather-SlackBot.git
   cd Weather-SlackBot
