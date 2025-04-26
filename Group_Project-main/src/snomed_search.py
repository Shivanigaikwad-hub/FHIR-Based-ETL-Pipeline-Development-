from pprint import pprint
import requests

BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed/concepts'


def get_basic_info(concept_id):
    """
    Fetches extended information for a given SNOMED CT concept ID.

    Parameters:
        concept_id (str): The SNOMED CT concept ID to retrieve information for.

    Returns:
        dict: The extended information of the concept, or an error message if the request fails.
    """
    try:
        # Construct the full URL
        url = f'{BASE_HERMES_URL}/{concept_id}'

        # Make the GET request
        response = requests.get(url)
        print(response.url)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            print(f'Effective time: {data["effectiveTime"]}')
            print(f'Concept ID: {data}["id"]')
        else:
            return {
                "error": f"Failed to fetch data. HTTP Status Code: {response.status_code}",
                "details": response.text
            }
    except requests.RequestException as e:
        # Handle network-related errors
        return {"error": "Network error occurred", "details": str(e)}


def get_concept_descriptions(concept_id):
    response = requests.get(f'{BASE_HERMES_URL}/{concept_id}/descriptions')
    print(response.url)
    data = response.json()
    for desc in data:
        status = "Active" if desc["active"] else "Inactive"
        effective_time = desc["effectiveTime"]
        term = desc["term"]
        print(f'{status} | Effective Time: {effective_time} | Term: {term}')


def get_extended(concept_id):
    response = requests.get(f'{BASE_HERMES_URL}/{concept_id}/extended')
    print(response.url)
    data = response.json()
    if "preferredDescription" in data:
        preferred_description = data["preferredDescription"]
        print(f'Preferred Description: {preferred_description["term"]}')
    else:
        print("Preferred description not available")

def get_parent_terms(concept_id):
    """
    Fetches the parent terms for a given SNOMED CT concept ID.

    Parameters:
        concept_id (str): The SNOMED CT concept ID.

    Returns:
        list: A list of parent terms, or an error message if none are found.
    """
    try:
        # Fetch the concept data
        response = requests.get(f'{BASE_HERMES_URL}/{concept_id}/extended')
        if response.status_code == 200:
            concept_data = response.json()

            # Get parent concept IDs under "116680003" (Is a relationship)
            parent_ids = concept_data.get("directParentRelationships", {}).get("116680003", [])

            if not parent_ids:
                return ["No parent terms found"]

            # Fetch preferred terms for each parent concept
            parent_terms = []
            for parent_id in parent_ids:
                parent_response = requests.get(f'{BASE_HERMES_URL}/{parent_id}/extended')
                if parent_response.status_code == 200:
                    parent_data = parent_response.json()
                    preferred_term = parent_data.get("preferredDescription", {}).get("term", "Unknown term")
                    parent_terms.append(preferred_term)
                else:
                    parent_terms.append(f"Failed to fetch details for parent ID {parent_id}")

            return parent_terms
        else:
            return [f"Failed to fetch concept data for {concept_id}. HTTP Status Code: {response.status_code}"]
    except requests.RequestException as e:
        return [f"Network error occurred: {e}"]

def constraint_parent(concept_id):
    """
    Create an ECL expression constraint to retrieve ascendants of a given SNOMED concept ID.
    """
    constraint = f"""
     >! {concept_id} | Parent |
    """
    return constraint


def constraint_child(concept_id):
    constraint = f"""
     <! {concept_id} | Child |
    """
    return constraint


def expression_constraint(search_string):
    """
    Perform a search using the SNOMED ECL constraint and print the concept ID and preferred term.
    """
    try:
        # Make the request
        response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string.strip()}')
        # Handle the response
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                concept_id = data[0]['conceptId']
                concept_preferred_term = data[0]['preferredTerm']
                return concept_id, concept_preferred_term
        else:
            print(f"Error: HTTP Status {response.status_code}")
            pprint(response.json())
    except requests.RequestException as e:
        print(f"Error: Network error occurred - {e}")



# Example usage:
if __name__ == "__main__":
    snomed_concept_id = "74400008"  # Replace with a valid concept ID
    #pprint(get_basic_info(concept_id=snomed_concept_id))
    # pprint(get_concept_descriptions(concept_id=snomed_concept_id))
    pprint(get_extended(concept_id=snomed_concept_id))
    # pprint(get_descendant_concepts(concept_id=snomed_concept_id))
    parent_terms = get_parent_terms(concept_id=snomed_concept_id)
    print("Parent Terms:", parent_terms)
    ascendant_constraint = constraint_parent(snomed_concept_id)
    print(f"Searching for ascendants of concept ID: {snomed_concept_id}")
    parent_concept_id = expression_constraint(search_string=ascendant_constraint)[0]
    parent_concept_term = expression_constraint(search_string=ascendant_constraint)[1]
    print(f'Parent:{parent_concept_id}')
    print(f'Parent term: {parent_concept_term}')

    child_constraint = constraint_child(concept_id=snomed_concept_id)
    child_terms = expression_constraint(search_string=child_constraint)
    child_concept_id = expression_constraint(search_string=child_constraint)[0]
    child_concept_term = expression_constraint(search_string=child_constraint)[1]
    print(f'Child:{child_concept_id}')
    print(f'Child term: {child_concept_term}')



