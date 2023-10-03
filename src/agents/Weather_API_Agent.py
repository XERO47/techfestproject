from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model
from utils import fetch_realtime_weather_data
class Location(Model):
    location: str
 
agent = Agent(
    name="agent",
    port=8001,
    seed="Weather agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(bob.wallet.address())
 
@agent.on_message(model=Location)
async def message_handler(ctx: Context, sender: str, loc: Location):
    ctx.logger.info(f"Received Coordinates from {sender}: {loc.location}")
    temperature=fetch_realtime_weather_data()
 
    await ctx.send(sender, Message(message="hello there alice"))
 
if __name__ == "__main__":
    agent.run()