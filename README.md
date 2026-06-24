# 💱 Forex Streaming Pipeline — AWS

Pipeline de dados em tempo real para monitoramento de cotações das 10 principais moedas do mundo contra o Real (BRL), construído com arquitetura Medallion completa na AWS.

---

## 🏗️ Arquitetura

EventBridge (1h) → Lambda → S3 Bronze (JSON) → EMR Serverless (PySpark) → S3 Silver → Gold BI e Gold ML

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
2. Se passarem, faz o deploy automático do script para o S3

---

## 📁 Estrutura do Projeto

pipeline/extract/extract.py — Lambda de extração

pipeline/extract/test_extract.py — 8 testes automatizados

pipeline/transform/transform.py — PySpark Silver + Gold BI + Gold ML

infra/main.tf — Recursos AWS via Terraform

.github/workflows/deploy.yml — CI/CD GitHub Actions

---

## 📊 Fonte dos Dados

ExchangeRate-API — atualização a cada hora