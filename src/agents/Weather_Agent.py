from uagents import Agent,Context

user=Agent(
    name="user",
    seed="user secret seed",
    port=8001
    endpoint="http://127.0.0.1/8001"
)

@user.on_interval(period=10)
async def call_agent_api(ctx: Context):
    