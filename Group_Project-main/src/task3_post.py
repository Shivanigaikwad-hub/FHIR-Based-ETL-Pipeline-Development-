import requests
import json
from pathlib import Path

# Base URL of the FHIR server
BASE_SERVER_URL = "http://137.184.71.65:8080/fhir"

# Directory containing the JSON file
data_dir = Path.cwd() / 'data'

def read_data(file_name):
    """Reads a JSON file."""
    json_file_path = data_dir / file_name
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        exit()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()

def post_observation(file_name, resource_name):
    """Posts an Observation resource to the FHIR server."""
    url = f"{BASE_SERVER_URL}/{resource_name}"
    data = read_data(file_name)

    # Define the headers
    headers = {
        "Content-Type": "application/json"
    }
    try:
        # Send the POST request
        response = requests.post(url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            print(f"Observation resource created successfully!")
            print("Response:", response.json())
        else:
            print(f"Failed to create Observation resource. Status code: {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")

if __name__ == "__main__":
    # Post the Observation resource
    post_observation(file_name='observation.json', resource_name='Observation')
