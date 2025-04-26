import json
from datetime import datetime
from pprint import pprint

import requests
from pathlib import Path
from data.datatemplates import condition_template_dict
from src.snomed_links import constraint_child, expression_constraint
from src.registration import data_dir
from src.TASK_1 import get_patient_resource_id
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
    if not access_token:
        raise ValueError("Access token is missing.")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers



def search_condition_second_child(patient_resource_id):
    """
    Retrieve the second condition for a patient and post a new condition with the child concept term.
    """
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        if 'entry' in data:
            conditions = data['entry']
            # Check if there are at least two conditions
            if len(conditions) > 1:
                second_condition = conditions[1]  # Retrieve the second condition
                snomed_code_from_openemr = second_condition["resource"]["code"]["coding"][0]["code"]
                print(f"Retrieved SNOMED code from the second condition: {snomed_code_from_openemr}")

                child_constraint = constraint_child(concept_id=snomed_code_from_openemr)
                child_concept_id, child_concept_term = expression_constraint(search_string=child_constraint)
                print(f"Identified Child Concept ID: {child_concept_id}")
                print(f"Identified Child Preferred Term: {child_concept_term}")

                condition_template_dict["code"]["text"] = child_concept_term
                condition_template_dict["code"]["coding"][0]["display"] = child_concept_term
                condition_template_dict["code"]["coding"][0]["code"] = child_concept_id
                condition_template_dict['verificationStatus']['coding'][0]['code'] = second_condition['resource']['verificationStatus']['coding'][0]['code']
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
                    url = f"{BASE_PRIMARY_CARE_URL}/Condition"
                    response = requests.post(url=url, json=condition_template_dict, headers=get_headers())
                    if response.status_code in [200, 201]:
                        print("New condition with child concept for the second term successfully posted to Primary Care EHR.")
                        print(f"Response Data: {response.json()}")
                    else:
                        print(f"Error creating child condition. Status Code: {response.status_code}, Error: {response.text}")
                except Exception as e:
                    print(f"Exception during condition creation: {e}")
            else:
                print("Less than two conditions found for the patient.")
        else:
            print("No entry key found in data.")
    else:
        print(f"Error fetching conditions. Status Code: {response.status_code}, Error: {response.text}")


if __name__ == "__main__":
    search_condition_second_child(patient_resource_id='985ac6fa-f55e-4796-b36d-9b7dd544e6fd')
