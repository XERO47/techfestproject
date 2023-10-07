# warning_trigger.py

# Import the necessary Streamlit functions
from streamlit import Server

# Define a function to trigger the warning in the Streamlit app
def trigger_warning(message):
    # Get the Streamlit server instance
    server = Server.get_current()

    # Call the display_warning function from app.py and pass the message
    server._session_context.session.get_main()._main_dg.file_context.script_request_queue.put_nowait({
        "type": "script",
        "payload": {
            "script_path": "frontend_components.py",
            "command": "generate_alert",
            "args": (message,),
            "kwargs": {},
        }
    })

if __name__ == "__main__":
    trigger_warning("12.34")
