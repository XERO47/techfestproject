import sys
from uagents import Agent,Context
sys.path.append('src')
from messages.converse import Location_share,Temperature_reply
from utils.alert_func import alert
user=Agent(
    name="user",
    seed="user secret seed",
    port=8002,
    endpoint="http://127.0.0.1/8002"
)
Weather_agent_address='agent1qfxwgdmmv90g62hd2hau7d8kc76tkrs8zfkd9zsnempmm3wy46zvkvfvvjp'
@user.on_interval(period=2)
async def call_agent_api(ctx: Context,):
    await ctx.send(Weather_agent_address,Location_share(location='pune'))
@user.on_message(model=Temperature_reply)
async def get_information(ctx: Context,temp:Temperature_reply):
    ctx.logger.info(temp.temprature)

    
if __name__ == "__main__":
    user.run()