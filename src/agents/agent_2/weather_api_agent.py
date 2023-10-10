import sys
import json
import requests
import os
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model

sys.path.append('src')
from utils.fetch import fetch_realtime_weather_data
from messages.converse import Location_share,Temperature_reply


agent = Agent(
    name="agent",
    seed="Weather agent secret phrase",
    # port=8001,
    # endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(agent.wallet.address())

@agent.on_message(model=Location_share)
async def agent_message_handler(ctx: Context, sender: str, loc: Location_share):
    
    ctx.logger.info(f"Received Coordinates from {sender}: {loc.lat,loc.lon}")
    intger=loc.num
    response=fetch_realtime_weather_data(f'{loc.lat},{loc.lon}')
    json_object=json.loads(response)
    current_temprature=json_object["current"]["temp_c"]
    
    await ctx.send(sender, Temperature_reply(temprature=f"{current_temprature}",num=f"{intger}"))
 
if __name__ == "__main__":
    agent.run()