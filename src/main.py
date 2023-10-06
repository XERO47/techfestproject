# main.py
import subprocess

def start_streamlit_app():
    subprocess.run(["streamlit", "run", "frontend/frontend_components.py"])

if __name__ == '__main__':
    start_streamlit_app()
