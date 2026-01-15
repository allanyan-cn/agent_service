import os
from pydantic import BaseModel, field_validator
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
import logging

os.environ['OPENAI_API_KEY'] = 'N/A'
os.environ['OPENAI_BASE_URL'] = 'http://localhost:1234/v1'

class WeatherRequest(BaseModel):
    city: str


class WeatherResult(BaseModel):
    city: str
    weather: str
    temperature_c: float

    @field_validator('weather')
    @classmethod
    def check_weather(cls, v):
        if v not in ["sunny", "cloudy", "overcast", "rain", "storm", "snow", "fog"]:
            logging.error("weather is unknown")
            raise ValueError("weather is unknown, weather should be in 'sunny', 'cloudy', 'overcast', 'rain', 'storm', 'snow', 'fog'")
        return v
    
    @field_validator('temperature_c')
    @classmethod
    def check_temperature(cls, v):
        if v >= 50 or v <= -50:
            raise ValueError("temperature is abnornal")
        return v


local_model = OpenAIChatModel(
    model_name="gpt-oss-20b",
    provider="openai",
    settings=ModelSettings(
        seed=42,
        temperature=0.0,
        timeout=300,
    ),
)

def get_weather(req: WeatherRequest) -> WeatherResult:
    logging.info(f"Call get_weather, city: {req.city}")
    response = WeatherResult(city=req.city, weather="sunn", temperature_c=25.5)
    logging.info(f"Return is {response}")
    return response

weather_agent = Agent[WeatherResult](
    model=local_model,
    system_prompt=(
        "You are a weather inquiry assistant."
        "Based on the city provided by the user, return the current weather conditions and temperature in Celsius via tools"
        "If the information cannot be determined, please state that clearly."
        "Please automatically correct spelling errors in output."
    ),
    tools=[get_weather],
    output_type=WeatherResult,
    retries=3
)
