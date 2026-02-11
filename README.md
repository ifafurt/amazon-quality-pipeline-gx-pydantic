🚀# Amazon Sales Data Quality Pipeline

This project implements an end-to-end Data Quality CI/CD Pipeline designed to automate validation checks for Amazon sales datasets. It ensures data integrity using industry-standard tools and provides real-time alerts via Slack.

🏗️ Architecture
The pipeline is triggered automatically on every code push to ensure that data quality is maintained throughout the development lifecycle.












graph TD
    A[Amazon Sale Report.csv] --> B{GitHub Actions CI}
    B --> C[gx_validation.py - Great Expectations]
    B --> D[pydantic_check.py - Pydantic]
    
    C --> E{Hata Var mı?}
    D --> E
    
    E -- Evet --> F[invalid_rows.csv Oluştur]
    E -- Evet --> G[Slack Bildirimi Gönder]
    
    E -- Hayır --> H[Pipeline Başarıyla Tamamlandı]





![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Data Quality](https://img.shields.io/badge/Data%20Quality-GX%20%26%20Pydantic-green)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)
    
