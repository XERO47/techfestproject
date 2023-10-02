from typing import Dict
from aiohttp import ClientSession
from datetime import datetime
from uagents import Agent, Context

class WeatherAgent(Agent):
    
    def __init__(self, _name, location, min_temp, max_temp, api_key):
        super().__init__(_name)
        self.location = location
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.api_key = api_key
        
    async def fetch_Weather_data(self, location: str, api_key: str) -> Dict:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        async with ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        
    async def on_interval(self, ctx: Context):
        ctx.logger.info(f"hitsuccess")
        weather_data = await self.fetch_Weather_data(self.location, self.api_key)
        current_temp = weather_data["main"]["temp"]
        if current_temp < self.min_temp or current_temp > self.max_temp:
            ctx.logger.info(f"Alert: Temperature in {self.location} is out of range!")
            
if __name__ == "__main__":
    agent = WeatherAgent("MyAgent", "New York", 10, 20, "my_api_key")
    agent.run()