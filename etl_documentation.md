<div style="display: flex; justify-content: space-between; align-items: center;">
  <h1>ETL Pipeline Documentation</h1>
  <img src="assets/ETL_logo.png" alt="ETL Vision Logo" style="width: 100px; height: auto;">
</div>

[Home](index.md) || [BPMN Model](bpmn.md) || [Use Case Model](use_case.md) || [ETL Pipeline](etl_documentation.md) || [Insights](insights.md) || [Team Contributions](team_contributions.md) || [About](about.md)


## Extraction:
- API Endpoint Details:
We used the OpenEMR FHIR API server to extract patient and condition data. Specifically, we accessed the /Patient and /Condition endpoints to gather information about patients and their medical conditions.

- Authentication Process:
Authentication was handled using Bearer tokens stored in a secure JSON file (access_token.json). These tokens were included in the HTTP headers for each API request to ensure secure and authorized access.

- Error Handling:
To make the system reliable, we added error-handling mechanisms to manage issues such as:

- Missing or invalid authentication tokens.
  
- Failed authentication attempts.
  
- Invalid API responses, such as "404 Not Found."
  
All errors were logged with clear and detailed messages, making it easier to debug and ensuring the process runs smoothly.

## Transformation

## Techniques for Cleaning and Formatting Data: 

- After extracting data from the OpenEMR API, a thorough review was conducted to ensure the data's completeness and accuracy. 

- Missing or irrelevant fields were identified and addressed to align with the requirements of the Primary EHR FHIR API. 

- Data formats were standardized, such as using ISO 8601 for date representations, and JSON structures were reformatted to comply with FHIR standards. 

## Tools Utilized: 

- Python’s json module played a pivotal role in parsing, formatting, and cleaning the extracted data. 

- SNOMED CT terms were retrieved through the HERMES API, ensuring adherence to accurate and consistent terminology standards. 


## Loading

## Process for Loading Data: 

- The cleaned and formatted data was uploaded to the Primary EHR FHIR API using HTTP POST requests. 

- Specific endpoints such as /Patient, /Condition, /Observation, and /Procedure were used to load corresponding resource types into the system. 

- Each API request included a header containing the access token for authentication and specified the content type as application/fhir+json to comply with FHIR standards. 

- Responses from the API were monitored to verify successful uploads, with particular attention to HTTP status codes 200 (OK) and 201 (Created).

## Coding Tasks

### **Task 1: Parent Concept Creation**

- We began by retrieving a patient and their conditions from the OpenEMR API. Using the concept ID from one condition, we located its parent term through the HERMES API. We automated the creation of a new Patient resource in the Primary EHR and linked a Condition resource referencing the parent concept.

```python
# Task 1: Parent Concept Creation
import json
import requests
from pprint import pprint

BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'
PRIMARY_EHR_BASE_URL = "http://137.184.71.65:8080/fhir"

# Function to get authorization headers
def get_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}

# Retrieve a patient from OpenEMR
def get_patient(patient_id, access_token):
    url = f"{BASE_URL}/Patient/{patient_id}"
    response = requests.get(url, headers=get_headers(access_token))
    if response.status_code == 200:
        print("Patient retrieved successfully.")
        return response.json()
    else:
        print(f"Failed to retrieve patient. Status code: {response.status_code}")
        return None

# Search for the patient's conditions
def search_condition(patient_id, access_token):
    url = f"{BASE_URL}/Condition?patient={patient_id}"
    response = requests.get(url, headers=get_headers(access_token))
    if response.status_code == 200:
        conditions = response.json()
        if 'entry' in conditions:
            first_condition = conditions['entry'][0]['resource']
            return first_condition['code']['coding'][0]['code']
        else:
            print("No conditions found.")
            return None
    else:
        print(f"Failed to retrieve conditions. Status code: {response.status_code}")
        return None

# Fetch the parent concept using HERMES API
def get_parent_concept(condition_code):
    constraint = f">! {condition_code}"
    url = f"{BASE_HERMES_URL}/search?constraint={constraint}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            print("Parent concept retrieved successfully.")
            return data[0]
    print("Failed to retrieve parent concept.")
    return None

# Create a new patient in the Primary EHR
def create_patient_in_ehr(patient_data, parent_concept_id, access_token):
    url = f"{PRIMARY_EHR_BASE_URL}/Patient"
    headers = get_headers(access_token)
    patient_data["extension"] = [
        {
            "url": "http://example.org/fhir/StructureDefinition/patient-parent-concept",
            "valueString": parent_concept_id
        }
    ]
    response = requests.post(url, headers=headers, json=patient_data)
    if response.status_code in [200, 201]:
        print("Patient created successfully in the Primary EHR.")
    else:
        print(f"Failed to create patient. Status code: {response.status_code}")

# Main Workflow
def task_1_workflow():
    access_token = "YOUR_ACCESS_TOKEN"  # Replace with actual token
    patient_id = "12345"  # Replace with actual patient ID

    patient_data = get_patient(patient_id, access_token)
    if patient_data:
        condition_code = search_condition(patient_id, access_token)
        if condition_code:
            parent_concept = get_parent_concept(condition_code)
            if parent_concept:
                create_patient_in_ehr(patient_data, parent_concept["conceptId"], access_token)

if __name__ == "__main__":
    task_1_workflow()
```

### **Task 2: Child Concept Creation
We reused the patient from Task 1. After retrieving a concept ID for one condition, we identified its child term through the HERMES API. A new Condition resource with the child concept was added to the Primary EHR.

```python
# Task 2: Child Concept Creation
import json
import requests
from pathlib import Path

# Define URLs and Headers
PRIMARY_EHR_BASE_URL = "http://137.184.71.65:8080/fhir"
BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'

def get_ehr_headers():
    # Retrieve EHR access token and headers
    pass

def expression_constraint(search_string):
    # Fetch child term using expression constraint
    response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string}')
    data = response.json()
    return {
        'conceptId': data[0]['conceptId'],
        'preferredTerm': data[0]['preferredTerm']
    }

def create_condition_in_primary_ehr(patient_id, child_term):
    # Create new condition resource in Primary EHR
    condition_resource = {
        "resourceType": "Condition",
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": child_term["conceptId"],
                "display": child_term["preferredTerm"]
            }],
            "text": child_term["preferredTerm"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        }
    }
    url = f"{PRIMARY_EHR_BASE_URL}/Condition"
    headers = get_ehr_headers()
    response = requests.post(url, headers=headers, json=condition_resource)
    return response.status_code
```

### **Task 3: Observation Creation

We created a Blood Pressure Observation (including systolic and diastolic values) using predefined data and standard codes. The Observation resource was then posted to the Primary EHR API.

```python
# Task 3: Observation Creation
def post_observation_to_primary_ehr(patient_id, observation_data):
    url = f"{PRIMARY_EHR_BASE_URL}/Observation"
    headers = get_ehr_headers()

    observation_data["subject"] = {"reference": f"Patient/{patient_id}"}

    response = requests.post(url, headers=headers, json=observation_data)
    if response.status_code in [200, 201]:
        print("Observation posted successfully.")
    else:
        print(f"Failed to post observation. Status code: {response.status_code}")

# Example Observation Data
observation_data = {
    "resourceType": "Observation",
    "status": "final",
    "category": [{"coding": [{"system": "http://loinc.org", "code": "vital-signs"}]}],
    "code": {"coding": [{"system": "http://loinc.org", "code": "85354-9"}]},
    "valueQuantity": {"value": 120, "unit": "mmHg"}
}
post_observation_to_primary_ehr("patient_id", observation_data)
```

### **Task 4: Procedure Creation

A Procedure resource (e.g., "Tooth Extraction") was created for the same patient from Task 1. This included essential details like the procedure type (SNOMED code), the practitioner performing it, and notes for the procedure. The Procedure resource was submitted to the Primary EHR API.

```python
# Task 4: Procedure Creation
def post_procedure_to_primary_ehr(patient_id, procedure_data):
    url = f"{PRIMARY_EHR_BASE_URL}/Procedure"
    headers = get_ehr_headers()

    procedure_data["subject"] = {"reference": f"Patient/{patient_id}"}

    response = requests.post(url, headers=headers, json=procedure_data)
    if response.status_code in [200, 201]:
        print("Procedure posted successfully.")
    else:
        print(f"Failed to post procedure. Status code: {response.status_code}")

# Example Procedure Data
procedure_data = {
    "resourceType": "Procedure",
    "status": "completed",
    "code": {
        "coding": [{"system": "http://snomed.info/sct", "code": "234724001", "display": "Tooth extraction"}]
    },
    "performer": [{"actor": {"reference": "Practitioner/4", "display": "Dr. Careful"}}],
    "note": [{"text": "Follow-up instructions provided. No complications observed."}]
}
post_procedure_to_primary_ehr("patient_id", procedure_data)
```

This workflow allowed us to extract, transform, and load clinical data into an EHR system efficiently. By automating the creation of patients, conditions, observations, and procedures, we demonstrated the importance of interoperability and automation in healthcare data management while adhering to FHIR standards.

## Challenges and Solutions

Authentication and Authorization:

Challenge: Expired or invalid access tokens caused API request failures.

Solution: Tokens were securely stored in a JSON file, and automated refresh mechanisms ensured valid tokens.
Error Handling:

Challenge: Invalid requests and failed uploads disrupted the workflow.

Solution: Detailed error messages and logging identified issues like invalid patient IDs or API endpoints.
Data Transformation:

Challenge: Mapping clinical terms to SNOMED concepts was complex due to hierarchical relationships.

Solution: Automated Python scripts retrieved and mapped SNOMED terms accurately.
Data Loading:

Challenge: Invalid payloads or missing fields caused upload failures.

Solution: Data was validated before loading, with logs and status codes (200 or 201) monitored for success.
Team Coordination:

Challenge: Ensuring smooth collaboration and task alignment.

Solution: Tasks were clearly divided, and regular check-ins resolved issues effectively.
