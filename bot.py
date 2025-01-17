from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import requests
import re
import openai
from bs4 import BeautifulSoup

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = App(token=SLACK_BOT_TOKEN)

# Function to fetch weather from OpenWeatherMap
def get_weather(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        if data.get("cod") != 200:
            return f"Sorry, I couldn't retrieve weather information: {data.get('message', 'Unknown error')}"

        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        location_name = data["name"]

        return f"The weather in {location_name} is {weather_description} with a temperature of {temperature}°C."

    except Exception as e:
        print(f"Primary weather API failed: {e}")
        return None

# Function to fetch weather from DuckDuckGo
def get_weather_from_duckduckgo(location):
    try:
        base_url = "https://html.duckduckgo.com/html/"
        search_query = f"weather in {location}"

        response = requests.post(base_url, data={"q": search_query})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        weather_snippet = soup.find("a", {"class": "result__snippet"})

        if weather_snippet:
            return f"DuckDuckGo Weather Info: {weather_snippet.text.strip()}"

        return "DuckDuckGo couldn't find weather information for this location."

    except Exception as e:
        print(f"DuckDuckGo weather fallback failed: {e}")
        return "Sorry, I couldn't retrieve weather information."


# Function to clean and sanitize the location
def sanitize_location(location):
    return location.strip().rstrip(",.?!")

# Event listener for messages
@app.event("message")
def handle_message_events(body, say):
    text = body.get("event", {}).get("text", "").lower()

    # Matching the pattern for weather queries
    match = re.search(r'how is the weather in (.+)', text)
    if match:
        location = match.group(1).strip()
        location = sanitize_location(location)

        print(f"Received location (raw): '{match.group(1)}'")
        print(f"Sanitized location: '{location}'")

        if location:
            weather_info = get_weather(location)  # Trying OpenWeatherMap API first
            if weather_info:
                print("Weather data retrieved from OpenWeatherMap API.")
            else:
                print("Primary weather API failed. Falling back to DuckDuckGo.")
                weather_info = get_weather_from_duckduckgo(location)   # Fallback to DuckDuckGo

            if weather_info:
                print("Weather information successfully retrieved.")
            else:
                print("Both weather APIs failed.")

            # Generate a GPT response if weather data is available
            if weather_info:
                gpt_prompt = f"Write a friendly and engaging response for: '{weather_info}'"
                gpt_response = generate_response_with_gpt(gpt_prompt)

                if gpt_response:
                    print("Response generated successfully using OpenAI GPT.")
                    say(gpt_response)
                else:
                    print("OpenAI GPT failed. Sending raw weather information.")
                    say(weather_info)
            else:
                say("Sorry, I couldn't retrieve weather information for this location.")

        else:
            print("No valid location found.")
            say("Oops! I couldn't find the location. Please try again.")

    elif "how is the weather" in text:
        say("Let me check the weather for you! Please provide a location, e.g., 'How is the weather in New York?'")
    else:
        say("I'm sorry, I didn't understand that. You can ask me about the weather by saying 'How is the weather in [city]?'")

# GPT model
def generate_response_with_gpt(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error generating response with GPT: {e}")
        return None


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
