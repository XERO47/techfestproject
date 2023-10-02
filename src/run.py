
from uagents import Agent, Context
def create_agent(location,min,max,i):
    
    agent = Agent(name="user_side", seed="user is the seed",port=800+i,endpoint="http://127.0.0.1:801/submit")
    
    a=agent.storage.set("location", f"{location}")
    a=agent.storage.set("min", f"{min}")
    a=agent.storage.set("max",f"{max}")
    
    @agent.on_interval(period=2)  # Check every 1 hour
    
    async def check_weather(ctx: Context):
        
        # Fetch weather data for 'location' from an API
        # Compare with min_temp and max_temp
        # Perform actions based on the comparison
        # You can send alerts, update a database, etc.
        None
    
    agent.run()
    return 
   

create_agent("mumbai","12","13",1)