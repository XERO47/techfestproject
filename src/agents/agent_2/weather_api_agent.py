import sys

import requests
import os
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model

sys.path.append('src')
from utils.fetch import fetch_realtime_weather_data
from messages.converse import Location_share,Temperature_reply








 
agent = Agent(
    name="agent",
    port=8001,
    seed="Weather agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(agent.wallet.address())
print(agent.address)
@agent.on_message(model=Location_share)
async def message_handler(ctx: Context, sender: str, loc: Location_share):
    ctx.logger.info(f"Received Coordinates from {sender}: {loc.location}")
    response=fetch_realtime_weather_data(f'{loc.location}')
    print(response)
 
    await ctx.send(sender, Temperature_reply(temprature=12.23))
 
if __name__ == "__main__":
    agent.run()