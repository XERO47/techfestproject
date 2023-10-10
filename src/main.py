# main.py
import subprocess
from agents.agent_1.Weather_Agent import user
from agents.agent_2.weather_api_agent import agent
from uagents import Bureau
import os
import time
# Get the current working directory (the folder containing this script)


# Specify the name of the file you want to execute
file_name = 'your_script.py'

def main():
    bureau=Bureau( port=8001,endpoint="http://127.0.0.1:8001/submit",)
    bureau.add(agent)
    bureau.add(user)
    
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    os.chdir(parent_dir)
    subprocess.Popen(["streamlit", "run", "src/frontend/frontend_components.py","--server.port","8600"])
    time.sleep(3)
    subprocess.Popen(["python", "src/utils/data_server.py",])
    time.sleep(3)
    bureau.run()
    
    print()
    

if __name__ == '__main__':
    main()
