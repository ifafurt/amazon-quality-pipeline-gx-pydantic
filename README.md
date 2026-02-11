# Amazon Sales Data Quality Pipeline🚀

This project implements an end-to-end Data Quality CI/CD Pipeline designed to automate validation checks for Amazon sales datasets. It ensures data integrity using industry-standard tools and provides real-time alerts via Slack.

🏗️ Architecture
The pipeline is triggered automatically on every code push to ensure that data quality is maintained throughout the development lifecycle.

graph TD

    A[Amazon Sale Report.csv] --> B{GitHub Actions CI}
    B --> C[gx_validation.py - Great Expectations]
    B --> D[pydantic_check.py - Pydantic]
    
    C --> E{Validation Failed?}
    D --> E
    
    E -- Yes --> F[Generate invalid_rows.csv]
    E -- Yes --> G[Send Slack Notification]
    
    E -- No --> H[Pipeline Success]



🛠️ Tech Stack
Python 3.11: Core programming logic.

Great Expectations (GX): Rule-based data validation.

Pydantic: Schema enforcement and data type validation.

GitHub Actions: Automated CI pipeline execution.

Slack API: Instant team notifications and alerting.

📋 Key Features

#1. Data Validation (Great Expectations)

The gx_validation.py script enforces critical business rules:

Uniqueness: Ensures Order ID contains no duplicates.

Consistency: Validates that the Status column only contains allowed categories (e.g., Shipped, Cancelled).

Completeness: Detects unexpected null values in mandatory fields.

#2. Schema Enforcement (Pydantic)

pydantic_check.py performs row-level validation to ensure:

Correct data types for every column.

All failed rows are automatically exported to invalid_rows.csv for further auditing.

#3. Automated CI/CD

Powered by GitHub Actions, the workflow:

Provisions a clean Ubuntu environment.

Installs dependencies from requirements.txt.

Executes validation scripts.

Reports status directly to the designated Slack channel.











![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Data Quality](https://img.shields.io/badge/Data%20Quality-GX%20%26%20Pydantic-green)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)
    
