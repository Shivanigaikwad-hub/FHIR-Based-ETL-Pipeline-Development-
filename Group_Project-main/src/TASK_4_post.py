import requests
import json
from pathlib import Path

# Define the base URL of the FHIR server
BASE_SERVER_URL = "http://137.184.71.65:8080/fhir"

# Define the directory for storing data files
data_dir = Path.cwd() / 'data'

def read_data(name_of_the_file):
    """
    Reads a JSON file and returns its content.
    :param name_of_the_file: Name of the file to read (without .json extension)
    :return: Parsed JSON content
    """
    json_file_path = data_dir / f"{name_of_the_file}.json"

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        exit()
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        exit()


def post_data(file_name, resource_name):
    """
    Posts data to the FHIR server for a given resource.
    :param file_name: Name of the JSON file containing the resource data
    :param resource_name: Name of the FHIR resource to post (e.g., "Procedure")
    """
    # Define the URL of the API endpoint
    url = f"{BASE_SERVER_URL}/{resource_name}"

    # Read data from the JSON file
    data = read_data(name_of_the_file=file_name)

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful
        if response.status_code in [200, 201]:
            print(f"{resource_name} resource posted successfully! Status Code: {response.status_code}")
            print("Response:", response.json())
        else:
            print(f"Failed to post {resource_name} resource. Status Code: {response.status_code}")
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


if __name__ == '__main__':
    # Post the Procedure resource using the function
    post_data(file_name='procedure', resource_name='Procedure')
