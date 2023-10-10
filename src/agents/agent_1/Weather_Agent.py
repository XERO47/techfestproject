import sys
from uagents import Agent,Context
import time
import requests
import os
from uagents.setup import fund_agent_if_low
sys.path.append('src')
from messages.converse import Location_share,Temperature_reply
from utils.alert_func import alert,gui_alert
from utils.mail_service import send_email

user=Agent(
    name="user",
    # port=8002,
    seed="user secret seed",
    # endpoint=["http://127.0.0.1:8002/submit"],
)
Weather_agent_address='agent1qfxwgdmmv90g62hd2hau7d8kc76tkrs8zfkd9zsnempmm3wy46zvkvfvvjp'
fund_agent_if_low(user.wallet.address())
latitudes =[] 
longitudes = []
min_temperatures = []
max_temperatures = []
status_flags=[]


# user.storage.set('status',[True])[0]
@user.on_interval(period=5)
async def call_agent_api(ctx: Context):
    
    
    url = "http://127.0.0.1:8080/get_json"  # Replace with the actual API endpoint
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract values from the JSON data
        latitudes = data.get('lat', [])
        longitudes = data.get('lon', [])
        min_temperatures = data.get('min_temp', [])
        max_temperatures = data.get('max_temp', [])
        status_flags = data.get('status', [])
        for i in range(len(latitudes)):
            
            lat=latitudes[i]
            lon=longitudes[i]     
            await ctx.send(Weather_agent_address,Location_share(lat=f'{lat}',lon=f"{lon}",num=f"{i}"))
    else:
       pass

@user.on_message(model=Temperature_reply)
async def get_information(ctx: Context,sender:str,temp:Temperature_reply):
    url = "http://127.0.0.1:8080/get_json"  # Replace with the actual API endpoint
    response = requests.get(url)

    
        # Parse the JSON response
    data = response.json()

    # Extract values from the JSON data
    latitudes = data.get('lat', [])
    longitudes = data.get('lon', [])
    min_temperatures = data.get('min_temp', [])
    max_temperatures = data.get('max_temp', [])
    status_flags = data.get('status', [])
    email = data.get('email', [])

    min_temp=min_temperatures[temp.num]
    max_temp=max_temperatures[temp.num]
    tempreture=int(temp.temprature)
    gen_alert=alert(min_temp,max_temp,tempreture)
    lat=str(latitudes[temp.num])
    lom=str(longitudes[temp.num])
    curr=str(temp.temprature)
    if(gen_alert==True ):
        if(status_flags[temp.num]==True):
           gui_alert(temp.temprature)
           array=status_flags
           modified_array = array[:temp.num] + [False] + array[temp.num + 1:]
           user.storage.set('status',modified_array)
           subject="Your Weather Agent alert was triggered"
           body=f"Your weather agent alert for Latitude:{lat} & Longitude:{lom} has been triggered, Current temperature for your location is {curr}"
           send_email(email[0],subject,body)
           print(f"Alert Triggred, Current Tempreture {temp.temprature}")
    else:
        pass
    ctx.logger.info(temp.temprature)
    


    
if __name__ == "__main__":
    user.run()