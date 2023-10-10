# Weather Alert System

**Weather Alert System** is a project that aims to provide weather alerts to users via email. We have integrated Uagents library with stream-lit and fast-api to make an `autonomous agents` to generate alert for weather conditions. It includes a streamlit frontend for GUI.


#### Table of Contents
* [Getting Started](#getting-started)
* [Installation](#installation)
  * [Windows](#windows)
  * [Set API key](#set-api-key)
* [Contributing](#contributing)
* [License](#license)
* [References](#references)

## Getting Started
To get started with the Weather Alert System, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Set the API key in .env file. Refer [Set API key](#set-api-key) for more information.
3. Run the application.
   ```bash
   python main.py
   ```

That's it! You should now be able to use the **Weather Alert System** to receive weather alerts via email.

**Note**:  Use light theme of `Streamlit` for better experience.



## Installation
### Windows
#### Step-1: Clone the repository.
```bash
git clone 
```
#### Step-2: Install the required dependencies.
Open a terminal in root directory of the repository and enter the following commands
```bash
poetry install
cd ./src
poetry shell
```
#### Step-3: Run the application.
```bash  
python main.py
```
Your application should start shortly.
### 
### Set API key

1. Create a `.env` file in the root directory of the repository.
2. 


## Contributing
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

