import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

PROMPT_TEMPLATE = """
You are a weather-based recommendation assistant.

Use the weather data below to generate:
1. outfit
2. activities
3. explanation

Rules:
- Return only valid JSON.
- Keep each value concise and practical.
- Do not include markdown.
- Do not include extra keys.

Required JSON format:
{
  "outfit": "string",
  "activities": "string",
  "explanation": "string"
}

Weather Data:
{weather_summary}
""".strip()

def validate_openai_key():
    if not OPENAI_API_KEY:
        raise ValueError("Missing OpenAI API key. Add OPENAI_API_KEY to the .env file.")

def get_ai_recommendation(weather, day):
    validate_openai_key()
    client = OpenAI(api_key=OPENAI_API_KEY)

    weather_summary = (
        f"Day: {day}\n"
        f"Condition: {weather['condition']}\n"
        f"Temperature: {weather['temp']}°F\n"
        f"Feels Like: {weather['feels_like']}°F\n"
        f"Humidity: {weather['humidity']}%\n"
        f"Wind Speed: {weather['wind_speed']} mph"
    )

    prompt = PROMPT_TEMPLATE.format(weather_summary=weather_summary)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Return structured JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("AI response was not valid JSON.")

    for key in ["outfit", "activities", "explanation"]:
        if key not in parsed:
            raise ValueError(f"AI response is missing the '{key}' field.")

    return parsed