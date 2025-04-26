import json
import random
from datetime import datetime
from pathlib import Path

import requests

from data.datatemplates import patient_template_dict, condition_template_dict
from src.registration import data_dir
from src.snomed_links import constraint_parent, expression_constraint

BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
BASE_PRIMARY_CARE_URL = "http://137.184.71.65:8080/fhir"
BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'

def get_access_token_from_file():
    file_path = Path(data_dir / "access_token.json")
    if not file_path.exists():
        print("Error: access_token.json file not found.")
        return None
    try:
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            access_token = json_data.get("access_token")
        return access_token
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error reading access token from file: {e}")
        return None


def get_headers():
    access_token = get_access_token_from_file()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers


def get_patient_resource_id():
    file_path = data_dir / "patient_resource_id.txt"
    try:
        with open(file_path, 'r') as file:
            resource_id = file.read().strip()
            return resource_id
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None


def get_fhir_patient(resource_id):
    url = f'{BASE_URL}/Patient/{resource_id}'
    response = requests.get(url=url, headers=get_headers())

    if response.status_code != 200:
        print(f"Failed to fetch patient. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return

    data = response.json()
    print("Response Data:", data)  # Debugging: Inspect the response structure

    # Check if 'name' field exists
    name_list = data.get("name", [])
    if not name_list:
        print("Error: 'name' field is missing or empty in the response.")
        return
    birth_date = data.get('birthDate')
    family_name = data['name'][0]['family']
    given_name = data['name'][0]['given'][0]
    possible_integers = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    address = data.get('address', [{}])[0]

    line = address.get('line', [''])[0]
    city = address.get('city', '')
    district = address.get('district', '-')
    state = address.get('state', '')
    postal_code = address.get('postalCode', '')
    text = f'{line}, {city}, {state}, {postal_code}'
    unique_patient_id = random.choice(possible_integers)
    today_date = datetime.today().date().isoformat()
    gender = data.get('gender')

    # Populate the patient template
    patient_template_dict["birthDate"] = birth_date
    patient_template_dict['name'][0]['family'] = family_name
    patient_template_dict['name'][0]['given'][0] = given_name
    patient_template_dict['address'][0]['line'][0] = line
    patient_template_dict['address'][0]['city'] = city
    patient_template_dict['address'][0]['district'] = district
    patient_template_dict['address'][0]['state'] = state
    patient_template_dict['address'][0]['postalCode'] = postal_code
    patient_template_dict['identifier'][0]['period']['start'] = today_date
    patient_template_dict['identifier'][0]['value'] = unique_patient_id
    patient_template_dict['gender'] = gender
    patient_template_dict['address'][0]['text'] = text
    try:
        headers = {
            "Accept": 'application/json'
        }
        url = BASE_PRIMARY_CARE_URL + '/' + 'Patient'
        response = requests.post(url=url, json=patient_template_dict, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            new_patient_resource_id = response_data['id']
            with open(data_dir / 'patient_resource_id.txt', 'w') as f:
                f.write(new_patient_resource_id)
        else:
            print('Error')
    except Exception as e:
        print(e)


def search_condition(patient_resource_id):
    """
    Create a condition resource on Primary Care EHR FHIR Server
    :return:
    """
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()

    if 'entry' in data:
        conditions = data['entry']
        # Process the second condition (if it exists)
        if len(conditions) > 1:
            second_condition = conditions[1]
            process_condition(second_condition, patient_resource_id)


def process_condition(condition_entry, patient_resource_id):
    """
    Create a condition resource based on the given condition entry.
    """
    snomed_code_from_openemr = condition_entry["resource"]["code"]["coding"][0]["code"]
    ascendant_constraint = constraint_parent(concept_id=snomed_code_from_openemr)
    parent_concept_id = expression_constraint(search_string=ascendant_constraint)[0]
    parent_concept_term = expression_constraint(search_string=ascendant_constraint)[1]

    condition_template_dict["code"]["text"] = parent_concept_term
    condition_template_dict["code"]["coding"][0]["display"] = parent_concept_term
    condition_template_dict["code"]["coding"][0]["code"] = parent_concept_id
    condition_template_dict['verificationStatus']['coding'][0]['code'] = condition_entry['resource']['verificationStatus']['coding'][0]['code']
    condition_template_dict["severity"]["coding"][0]["system"] = "http://snomed.info/sct"
    condition_template_dict["severity"]["coding"][0]["code"] = "N/A"
    condition_template_dict["severity"]["coding"][0]["display"] = "Not Applicable"
    condition_template_dict["bodySite"][0]["coding"][0]["system"] = "http://snomed.info/sct"
    condition_template_dict["bodySite"][0]["coding"][0]["code"] = "N/A"
    condition_template_dict["bodySite"][0]["coding"][0]["display"] = "Not Applicable"
    condition_template_dict["bodySite"][0]["text"] = "Not Applicable"
    condition_template_dict["onsetDateTime"] = datetime.today().date().isoformat()
    primary_care_resource_id = get_patient_resource_id()
    condition_template_dict['subject']['reference'] = f"Patient/{primary_care_resource_id}"

    try:
        headers = {
            "Accept": 'application/json'
        }
        url = f"{BASE_PRIMARY_CARE_URL}/Condition"
        response = requests.post(url=url, json=condition_template_dict, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            print(response_data)
        else:
            print(f"Failed to create condition. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get_fhir_patient(resource_id='985ac6fa-f55e-4796-b36d-9b7dd544e6fd')
    search_condition(patient_resource_id='985ac6fa-f55e-4796-b36d-9b7dd544e6fd')
