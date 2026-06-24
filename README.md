# 💱 Forex Streaming Pipeline — AWS

End-to-end data pipeline for real-time monitoring of the 10 most traded currencies against the Brazilian Real (BRL), built with Medallion Architecture on AWS.

---

## 🏗️ Architecture

EventBridge (1h) → Lambda → S3 Bronze (JSON) → EMR Serverless (PySpark) → S3 Silver → Gold BI and Gold ML

---

## 💰 Currencies Monitored

USD, EUR, JPY, GBP, AUD, CAD, CHF, CNY, HKD, SEK — all vs BRL

---

## 📦 Data Layers

| Layer | Format | Description |
|-------|--------|-------------|
| Bronze | JSON | Raw API data, partitioned by date |
| Silver | Parquet | Clean, validated and enriched data |
| Gold BI | Parquet | Dimensional modeling for dashboards |
| Gold ML | Parquet | Feature Store for machine learning models |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Extraction | AWS Lambda + Python |
| Scheduling | Amazon EventBridge |
| Storage | Amazon S3 |
| Processing | EMR Serverless + PySpark |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Credentials | AWS Secrets Manager |

---

## ✅ Data Quality

Validations implemented at extraction time:

- Minimum volume of 10 currencies per execution
- Invalid exchange rates (zero or null values)
- Empty timestamps
- Duplicate currency records

---

## 🚀 CI/CD

On every push to the pipeline/ folder, GitHub Actions:

1. Runs 8 automated tests (pytest)
2. If all pass, deploys the script automatically to S3

---

## 📁 Project Structure

pipeline/extract/extract.py — Lambda extraction function

pipeline/extract/test_extract.py — 8 automated tests

pipeline/transform/transform.py — PySpark Silver + Gold BI + Gold ML

infra/main.tf — AWS resources via Terraform

.github/workflows/deploy.yml — GitHub Actions CI/CD

---

## 📊 Data Source

ExchangeRate-API — hourly updates