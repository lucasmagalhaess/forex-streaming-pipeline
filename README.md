# 💱 Forex Streaming Pipeline — AWS

Pipeline de dados em tempo real para monitoramento de cotações das 10 principais moedas do mundo contra o Real (BRL), construído com arquitetura Medallion completa na AWS.

---

## 🏗️ Arquitetura

\\\
EventBridge (1h) → Lambda → S3 Bronze (JSON)
                              ↓
                         EMR Serverless (PySpark)
                              ↓
                    S3 Silver (Parquet limpo)
                              ↓
              ┌───────────────────────────────┐
              ↓                               ↓
   S3 Gold BI (Star Schema)     S3 Gold ML (Feature Store)
\\\

---

## 💰 Moedas Monitoradas

USD, EUR, JPY, GBP, AUD, CAD, CHF, CNY, HKD, SEK — todas vs BRL

---

## 📦 Camadas de Dados

| Camada | Formato | Descrição |
|--------|---------|-----------|
| Bronze | JSON | Dado bruto da API, particionado por data |
| Silver | Parquet | Dado limpo, validado e enriquecido |
| Gold BI | Parquet | Modelagem dimensional para dashboards |
| Gold ML | Parquet | Feature Store para modelos de ML |

---

## 🛠️ Stack Tecnológica

| Categoria | Tecnologia |
|-----------|------------|
| Extração | AWS Lambda + Python |
| Agendamento | Amazon EventBridge |
| Storage | Amazon S3 |
| Processamento | EMR Serverless + PySpark |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Credenciais | AWS Secrets Manager |

---

## ✅ Qualidade de Dados

Validações implementadas na extração:
- Volume mínimo de 10 moedas por execução
- Cotações inválidas (zero ou nulas)
- Timestamps vazios
- Moedas duplicadas

---

## 🚀 CI/CD

A cada push na pasta pipeline/, o GitHub Actions:
1. Roda os 8 testes automatizados (pytest)
2. Se passarem → deploy automático do script para o S3

---

## 📁 Estrutura do Projeto

\\\
forex-streaming-pipeline/
├── pipeline/
│   ├── extract/
│   │   ├── extract.py
│   │   └── test_extract.py
│   └── transform/
│       └── transform.py
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── .github/
    └── workflows/
        └── deploy.yml
\\\

---

## 📊 Fonte dos Dados

[ExchangeRate-API](https://www.exchangerate-api.com/) — atualização a cada hora
