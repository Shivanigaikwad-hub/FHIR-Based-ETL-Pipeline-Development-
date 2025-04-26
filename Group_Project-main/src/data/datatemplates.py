patient_template_dict = {
    "resourceType": "Patient",
    "identifier": [
        {
            "use": "usual",
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR"
                    }
                ]
            },
            "system": "urn:oid:1.2.36.146.595.217.0.1",
            "value": "",  # Example medical record ID
            "period": {
                "start": ""  # Example start date
            }
        }
    ],
    "active": True,
    "name": [
        {
            "use": "official",
            "family": "",
            "given": [
                ""
            ]
        }
    ],
    "gender": "",
    "birthDate": "",
    "deceasedBoolean": False,
    "address": [
        {
            "use": "home",
            "type": "both",
            "text": "",
            "line": [
                ""
            ],
            "city": "",
            "district": "",
            "state": "",
            "postalCode": "",
            "period": {
                "start": ""  # Example address start date
            }
        }
    ]
}

condition_template_dict = {
    "resourceType": "Condition",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "unconfirmed"  # Example verification status
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                },
                {
                    "system": "http://snomed.info/sct",
                    "code": "439401001",
                    "display": "Diagnosis"
                }
            ]
        }
    ],
    "severity": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "",  # Example severity code for "Severe"
                "display": ""
            }
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "",  # Example SNOMED CT code for "Appendicitis"
                "display": ""
            }
        ],
        "text": ""
    },
    "bodySite": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "",  # Example body site code for "Abdomen"
                    "display": ""
                }
            ],
            "text": ""
        }
    ],
    "subject": {
        "reference": ""  # Reference to the patient resource
    },
    "onsetDateTime": ""
}


