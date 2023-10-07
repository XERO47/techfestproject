from uagents import Model

class Location_share(Model):
    lat: str
    lon: str
    num: int

class Temperature_reply(Model):
    temprature: float
    num: int