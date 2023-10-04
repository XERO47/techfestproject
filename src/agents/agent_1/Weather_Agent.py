import sys
from uagents import Agent,Context
from uagents.setup import fund_agent_if_low
sys.path.append('src')
from messages.converse import Location_share,Temperature_reply
from utils.alert_func import alert
user=Agent(
    name="user",
    port=8002,
    seed="user secret seed",
    endpoint=["http://127.0.0.1:8002/submit"],
)
Weather_agent_address='agent1qfxwgdmmv90g62hd2hau7d8kc76tkrs8zfkd9zsnempmm3wy46zvkvfvvjp'
fund_agent_if_low(user.wallet.address())

def parse_json_file(file):
    
@user.on_interval(period=2)
async def call_agent_api(ctx: Context,):
    await ctx.send(Weather_agent_address,Location_share(location='pune'))
@user.on_message(model=Temperature_reply)
async def get_information(ctx: Context,sender:str,temp:Temperature_reply):

    ctx.logger.info(temp.temprature)

    
if __name__ == "__main__":
    user.run()