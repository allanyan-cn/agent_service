import os
from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel

os.environ['OPENAI_API_KEY'] = 'N/A'
os.environ['OPENAI_BASE_URL'] = 'http://localhost:1234/v1'

class WeatherRequest(BaseModel):
    city: str


class WeatherResult(BaseModel):
    city: str
    weather: str
    temperature_c: float


local_model = OpenAIChatModel(
    model_name="gpt-oss-20b",
    provider="openai",
    settings=ModelSettings(
        seed=42,
        temperature=0.0
    ),
)

weather_agent = Agent[WeatherResult](
    model=local_model,
    system_prompt=(
        "You are a weather inquiry assistant."
        "Based on the city provided by the user, return the current weather conditions and temperature in Celsius."
        "If the information cannot be determined, please state that clearly."
        "Please return the response strictly in JSON format."
    ),
)
