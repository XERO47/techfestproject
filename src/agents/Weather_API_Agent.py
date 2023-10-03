from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model
from messages import Location_share,Temperature_reply

import os

api_key=os.getenv('Weather_API_key')
def fetch_realtime_weather_data(location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)




 
agent = Agent(
    name="agent",
    port=8001,
    seed="Weather agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(agent.wallet.address())
 
@agent.on_message(model=Location)
async def message_handler(ctx: Context, sender: str, loc: Location,temp: Temperature_reply):
    ctx.logger.info(f"Received Coordinates from {sender}: {loc.location}")
    response=fetch_realtime_weather_data(f'{loc.location}')

 
    await ctx.send(sender, Temperature_reply(temp=12.23))
 
if __name__ == "__main__":
    agent.run()