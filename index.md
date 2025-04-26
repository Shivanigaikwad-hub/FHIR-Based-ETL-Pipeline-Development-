<div style="display: flex; justify-content: space-between; align-items: center;">
  <h1>Home</h1>
  <img src="assets/ETL_logo.png" alt="ETL Vision Logo" style="width: 100px; height: auto;">
</div>

## Welcome to the ETL VISION Project

This is the home page for the ETL VISION Project. Explore the links below to learn more about the project.

[Home](./index.md) ||
[BPMN Model](./bpmn.md) ||
[Use Case Model](./use_case.md) ||
[ETL Pipeline](./etl_documentation.md) ||
[Insights](./insights.md) ||
[Team Contributions](./team_contributions.md) ||
[About](./about.md) ||

![project_overview_image](./assets/project_overview.png)

## Introduction

Our project demonstrates the creation and implementation of an ETL (Extract, Transform, Load) pipeline for healthcare data integration using FHIR APIs, a standard format for healthcare data exchange. This project simulates real-world scenarios to showcase how systems can effectively exchange and process patient information. It highlights the importance of FHIR standards in ensuring consistency and interoperability across healthcare systems.

## Purpose of the ETL Pipeline

The ETL pipeline is essential for integrating data between healthcare systems. It automates the retrieval of patient data from one system, transforms it into the format required by another, and loads it into the target system. This project showcases how healthcare organizations can streamline workflows, improve data accuracy, and ensure timely access to patient information, enhancing decision-making and patient care.

![project_overview_image](./assets/ETL_process.png)

## Key Tools and Technologies

Programming Language:

## Python: 
- Used to build and automate the ETL pipeline.

## APIs:

- FHIR API: A standardized protocol for healthcare data exchange.
- OpenEMR FHIR API: For extracting patient and condition data.
- Hermes Terminology Server: To fetch related parent and child terms for medical concepts (SNOMED).
- Primary Care EHR FHIR API: The target system for loading transformed data.

## Python Libraries:

- requests: For API communication.
- json: For parsing and manipulating JSON data.
- Matplotlib: For creating visualizations like bar charts to represent project insights.

## Visualization Tools:

- Canva: For creating polished and creative visual content.
- Lucidchart: For crafting professional diagrams, including use case diagrams.
- Matplotlib: For generating project-specific data visualizations.

## Diagram Creation:

- Camunda: Used for designing the BPMN (Business Process Model and Notation) diagrams to visualize workflows.
- Lucidchart: Used for creating use case diagrams to represent actor and system interactions.

## Version Control and Hosting:

- GitHub: Used for version control, project collaboration, and organization.
- GitHub Markdown: For writing and formatting documentation in repositories.
- GitHub Pages: Used for hosting the project website with a professional presentation of documentation and insights.




## Summary of Deliverables

This project shows how Python and FHIR APIs were used to manage and integrate healthcare data effectively. We created Python scripts to perform four key tasks: extracting patient and condition data, retrieving parent and child terms for medical conditions, and creating resources like Patient, Condition, Observation, and Procedure in the Primary Care EHR FHIR server.

All project files, including the Python scripts, a README file, and documentation, are available in our GitHub repository. The repository is linked to a GitHub Pages website that includes sections like the project overview, BPMN model, use case diagram, ETL process documentation, and visual insights.

The BPMN model explains the process of patient referrals and treatments between primary care clinics and hospitals. The use case diagram shows how different users, like primary care providers and specialists, interact with the system. We also documented challenges such as handling API errors and inconsistent data, along with how we solved them.

This project highlights the importance of teamwork and technical skills while demonstrating how automation and standardized data exchange improve healthcare workflows. By completing this project, we proved how FHIR standards and Python-based automation can solve real-world problems in healthcare data management.
