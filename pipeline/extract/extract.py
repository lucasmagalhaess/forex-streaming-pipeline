import boto3
import json
import requests
from datetime import datetime, timezone


MOEDAS = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "SEK"]
SECRET_NAME = "forex-pipeline/api-key"




def get_secret(secret_name, region="us-east-1"):
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def get_cotacoes(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/BRL"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def filtrar_moedas(dados):
    cotacoes = dados["conversion_rates"]
    timestamp_api = dados["time_last_update_utc"]
    timestamp_netxattapi = dados["time_next_update_utc"]
    timestamp_coleta = datetime.now(timezone.utc).isoformat()

    registros = []
    for moeda in MOEDAS:
        registro = {
            "moeda" : moeda,
            "cotacao_brl" : cotacoes[moeda],
            "timestamp_coleta" : timestamp_coleta,
            "timestamp_api" : timestamp_api,
            "timestamp_nextattapi" : timestamp_netxattapi

        }
        registros.append(registro)

    return registros


def validar_registros(registros):
    total = len(registros)

    # Volume mínimo
    if total < 10:
        raise ValueError(f"API retornou apenas {total} moedas - esperado 10!")
    
    for r in registros:
        # Cotação vazia ou zero
        if not r["cotacao_brl"] or r["cotacao_brl"] <= 0:
            raise ValueError(f"Cotação inválida para {r['moeda']}: {r['cotacao_brl']}")
        
        # Datas Vazias 
        if not r["timestamp_api"] or not r["timestamp_nextattapi"]:
            raise ValueError(f"Timestamp vazio para {r['moeda']}")
        
    # Moeda duplicada
    moedas = [r["moeda"] for r in registros]
    duplicadas = [m for m in moedas if moedas.count(m) > 1]
    duplicadas = list(set(duplicadas))

    if duplicadas:
        raise ValueError(f"Moedas duplicadas detectadas: {duplicadas}")