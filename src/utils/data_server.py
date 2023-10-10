from fastapi import FastAPI
import json
import sys
sys.path.append('src')

app = FastAPI()
# Define a route to serve the JSON file
@app.get("/get_json")
async def get_json():
    
    # Read the JSON file
    with open("src/agent1qfu86j53jq_data.json", "r") as file:
        
        data = json.load(file)
    
    return data  # Return the JSON data as the response

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
