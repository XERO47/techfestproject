from uagents import Agent, Context

import utils.fetch as fetch_Weather_data
class WeatherAgent(Agent):
    
    def __init__(self, _name, location, min_temp, max_temp, api_key):
        super().__init__(_name)
        self.location = location
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.api_key = api_key
        
    @Agent.on_interval(self,period=3600)  # Check every hour
    async def check_weather(self, ctx: Context):
        ctx.logger.info(f"hitsuccess")
        weather_data = fetch_Weather_data(self.location, self.api_key)
        current_temp = weather_data["main"]["temp"]
        if current_temp < self.min_temp or current_temp > self.max_temp:
            ctx.logger.info(f"Alert: Temperature in {self.location} is out of range!")

agent=WeatherAgent("agg")
agent.run()

