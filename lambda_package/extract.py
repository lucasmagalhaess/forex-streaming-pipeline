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

    # Volume mÃ­nimo
    if total < 10:
        raise ValueError(f"API retornou apenas {total} moedas - esperado 10!")
    
    for r in registros:
        # CotaÃ§Ã£o vazia ou zero
        if not r["cotacao_brl"] or r["cotacao_brl"] <= 0:
            raise ValueError(f"CotaÃ§Ã£o invÃ¡lida para {r['moeda']}: {r['cotacao_brl']}")
        
        # Datas Vazias 
        if not r["timestamp_api"] or not r["timestamp_nextattapi"]:
            raise ValueError(f"Timestamp vazio para {r['moeda']}")
        
    # Moeda duplicada
    moedas = [r["moeda"] for r in registros]
    duplicadas = [m for m in moedas if moedas.count(m) > 1]
    duplicadas = list(set(duplicadas))

    if duplicadas:
        raise ValueError(f"Moedas duplicadas detectadas: {duplicadas}")
    
    print(f"✅ {total} moedas validadas com sucesso")
    return registros  # ← essa linha precisa estar aqui
    

def salvar_bronze(registros):
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")

    payload = {
        "extraction_date": today,
        "extraction_timestamp": timestamp,
        "total_registros": len(registros),
        "registros": registros
    }

    s3 = boto3.client("s3")
    bucket = "forex-streaming-datalake-dev"
    key = f"bronze/forex/data={today}/cotacoes_{timestamp}.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(payload, ensure_ascii=False, indent=2),
        ContentType="application/json"
    )

    print(f"✅ Bronze salvo: s3://{bucket}/{key}")
    return key


def extract(event=None, context=None):
    print("🚀 Iniciando extração de cotações forex...")
    
    # 1. Busca credenciais
    credenciais = get_secret(SECRET_NAME)
    api_key = credenciais["api_key"]
    print("✅ Credenciais carregadas")

    # 2. Chama a API
    dados = get_cotacoes(api_key)
    print("✅ Dados recebidos da API")

    # 3. Filtra as 10 moedas
    registros = filtrar_moedas(dados)
    print(f"✅ {len(registros)} moedas filtradas")

    # 4. Valida integridade
    registros = validar_registros(registros)

    # 5. Salva no Bronze
    key = salvar_bronze(registros)

    print(f"\n✅ Extração concluída! Arquivo salvo em: {key}")
    return key


if __name__ == "__main__":
    extract()