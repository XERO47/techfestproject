# Weather Alert System

**Weather Alert System** is a project that aims to provide weather alerts to users via email. We have integrated Uagents library with stream-lit and fast-api to make an `autonomous agents` to generate alert for weather conditions. It includes a streamlit frontend for GUI.


#### Table of Contents
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Contributing](#contributing)
* [License](#license)
* [References](#references)

## Getting Started 🤖
To get started with the Weather Alert System, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Set the API key in .env file. Refer [Installation](#installation) for more information.
3. Run the application.
   
   ```bash
   python main.py
   ```

That's it! You should now be able to use the **Weather Alert System** to receive weather alerts via email.

**Note**:  Use light theme of `Streamlit` for better experience.



## Installation 🎁

### Step-1: Obtain API Keys
Before running the agents, you need to obtain the required API keys:

#### WEATHER_API_KEY

1. Visit the Weatherapi website: https://www.weatherapi.com/
2. If you don't have an account, create one by signing up.
3. Verification mail will be sent to your gmail, verify the same.
4. Once you logged into your account, you will see on top to copy your `API-Key`.
   
### Step-2: Set Environment Variables
1. We have provided you with `.env-example` file in the root directory of the repository.
2. Change the file name to `.env` and paste your `API-key` in there.
   
   ```bash
   Weather_API_key="<Enter your API key here>"
   ```
### Step-3: Install Dependencies
* Clone the repository using:
  
   ```bash
   git clone https://github.com/AyushSenDazzler/HackAI_Hack-230459.git
   ```
* Open a terminal in root directory of the repository and enter the following commands
  
  ```bash
  poetry install
  cd ./src
  poetry shell
  ```
### Step-4: Run the application.
* To run project and its agents:

  ```bash  
  python main.py
  ```
Your application should start shortly. Now you have stream-lit app and the agents up and running 🎉.

## ✨Contributing
The guidelines for contributing to the project can be found in the [CONTRIBUTING.md]() file. It is recommended to follow these guidelines to ensure that contributions are consistent and meet the project's standards.

**Team Lead**:  Ayush Kumar
   
**Team members**: Abhishek Patil

## License
This project is available under the [MIT License](
).
## References

* [Uagents](https://fetch.ai/docs)
* [Streamlit](https://docs.streamlit.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [OpenWeatherMap](https://openweathermap.org/api)

