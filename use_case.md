<div style="display: flex; justify-content: space-between; align-items: center;">
  <h1>Use Case</h1>
  <img src="assets/ETL_logo.png" alt="ETL Vision Logo" style="width: 100px; height: auto;">
</div>

[Home](index.md) || [BPMN Model](bpmn.md) || [Use Case Model](use_case.md) || [ETL Pipeline](etl_documentation.md) || [Insights](insights.md) || [Team Contributions](team_contributions.md) || [About](about.md)

## Use Case Diagram

![Use Case Diagram](./assets/use_case.png)

## Description

The actors depicted in this use case diagram are the Primary care clinic, Patient, Hospital administration staff and CDSS. The use cases of the primary care clinic include sending the patient referral to the hospital and receiving the patient’s treatment details and decisions made from the hospital. An extension point is created for a scenario indicating an incomplete patient information sent to the hospital, which triggers a use case from the hospital admin staff requesting for additional information. The use case for the hospital admin staff also includes receiving the patient referral from the hospital, recording and storing the patient’s information in the EHR, and sending the patient’s treatment details and decisions to the primary care clinic. An include relationship exists from “receive patient referral” to “record and store patient’s information in the EHR”. The patient’s use cases include getting referred, providing information to be recorded or updated to the EHR, undergo specialist evaluation, receives treatment and follow specialist discharge instructions or follow-up recommendations.
The use case of the CDSS includes analyzing the patient’s information in the EHR and recommending one out of two outcomes; refer patient to primary care clinic for follow-up treatment or discharge if no further treatment is required. The refer patient for follow-up treatment has an extension point to the use case refer patient linked to the specialist while the discharge patient if no further treatment is required has an extension point to the use case discharge patient linked to the specialist. Both recommendations were highlighted in the diagram to show the possible outcomes, with extension points for use cases to the specialist indicating that the final decision is made by the specialist based on the recommendation of the CDSS if the required conditions are met. The use case “update the EHR” has an include relationship linked to “discharge patient” and “refer to primary care clinic”, this means in a case where either decision is implemented, the process involves updating the decision in the patient’s EHR. The use case “evaluate and document findings in the EHR” has an extend relationship to “request additional tests”, indicating a scenario where additional tests are required for proper evaluation.

