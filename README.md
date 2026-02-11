# Amazon Sales Data Quality Pipeline🚀

This project implements an end-to-end Data Quality CI/CD Pipeline designed to automate validation checks for Amazon sales datasets. It ensures data integrity using industry-standard tools and provides real-time alerts via Slack.

# 🏗️ Architecture
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



# 🛠️ Tech Stack
Python 3.11: Core programming logic.

Great Expectations (GX): Rule-based data validation.

Pydantic: Schema enforcement and data type validation.

GitHub Actions: Automated CI pipeline execution.

Slack API: Instant team notifications and alerting.

# 📋 Key Features

# 1. Data Validation (Great Expectations)
The gx_validation.py script enforces critical business rules:

Uniqueness: Ensures Order ID contains no duplicates.

Consistency: Validates that the Status column only contains allowed categories (e.g., Shipped, Cancelled).

Completeness: Detects unexpected null values in mandatory fields.

<img width="695" height="280" alt="Screenshot 2026-02-11 234743" src="https://github.com/user-attachments/assets/93330b84-fc7f-454a-86b6-e3e0cb2bb3a4" />

---
# 2. Schema Enforcement (Pydantic)
pydantic_check.py performs row-level validation to ensure:

Correct data types for every column.

All failed rows are automatically exported to invalid_rows.csv for further auditing.

<img width="535" height="154" alt="Screenshot 2026-02-12 000036" src="https://github.com/user-attachments/assets/c9224e89-45da-4802-b1d8-e0973bffc533" />

---
# 3. Automated CI/CD
Powered by GitHub Actions, the workflow:

Provisions a clean Ubuntu environment.

Installs dependencies from requirements.txt.

Executes validation scripts.

Reports status directly to the designated Slack channel.

<img width="844" height="797" alt="Screenshot 2026-02-12 000334" src="https://github.com/user-attachments/assets/2ac59342-caae-4ace-abe5-2da7e231538b" />

---

<img width="1038" height="609" alt="Screenshot 2026-02-12 001807" src="https://github.com/user-attachments/assets/3bc6b671-c95f-479e-aa4c-67fef391f8f3" />

---

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Data Quality](https://img.shields.io/badge/Data%20Quality-GX%20%26%20Pydantic-green)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)
    
