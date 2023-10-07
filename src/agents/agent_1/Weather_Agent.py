import sys
from uagents import Agent,Context
import time
import streamlit as st
from uagents.setup import fund_agent_if_low
sys.path.append('src')
from messages.converse import Location_share,Temperature_reply
from utils.alert_func import alert
from frontend.frontend_components import *
user=Agent(
    name="user",
    # port=8002,
    seed="user secret seed",
    # endpoint=["http://127.0.0.1:8002/submit"],
)
Weather_agent_address='agent1qfxwgdmmv90g62hd2hau7d8kc76tkrs8zfkd9zsnempmm3wy46zvkvfvvjp'
fund_agent_if_low(user.wallet.address())



# user.storage.set('status',[True])[0]
@user.on_interval(period=5)
async def call_agent_api(ctx: Context):
    if(ctx.storage.get('lat',)==None):
        pass
    else:
       for i in range(len(ctx.storage.get('lat',))):
           lat=ctx.storage.get('lat')[i]
           lon=ctx.storage.get('lon')[i]     
           await ctx.send(Weather_agent_address,Location_share(lat=f'{lat}',lon=f"{lon}",num=f"{i}"))
        #    time.sleep(10)
@user.on_message(model=Temperature_reply)
async def get_information(ctx: Context,sender:str,temp:Temperature_reply):
    min_temp=ctx.storage.get('min_temp')[temp.num]
    max_temp=ctx.storage.get('max_temp')[temp.num]
    gen_alert=alert(min_temp,max_temp,temp.temprature)
    print(gen_alert)
    if(gen_alert==True):
        generate_alert(temp.temprature)
        # st.warning("ohk go up baby")
        print(f"alert Up...............{temp.temprature}")
    else:
        pass
    ctx.logger.info(temp.temprature)
    


    
if __name__ == "__main__":
    user.run()