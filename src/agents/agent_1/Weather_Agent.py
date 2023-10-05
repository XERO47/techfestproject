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

user.storage.set("lat",[12,13,14])
user.storage.set("lon",[12,13,14])
print(user.storage.get("lat")[0])
# for i in 
#     print(f"{lat}")


@user.on_interval(period=120)
async def call_agent_api(ctx: Context,):
    for i in range(len(ctx.storage.get('lat'))):
        lat=ctx.storage.get('lat')[i]
        lon=ctx.storage.get('lon')[i]     
    await ctx.send(Weather_agent_address,Location_share(lat=f'{lat}',lon=f"{lon}"))

    
@user.on_message(model=Temperature_reply)
async def get_information(ctx: Context,sender:str,temp:Temperature_reply):

    ctx.logger.info(temp.temprature)

    
if __name__ == "__main__":
    user.run()