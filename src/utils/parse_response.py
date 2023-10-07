
def parse_resposne(data):
    temperature_celsius = data["current"]["temp_c"]
    print(type(temperature_celsius))
    return temperature_celsius
