from extract import filtrar_moedas
from extract import filtrar_moedas, validar_registros
from unittest.mock import patch, MagicMock
import pytest




DADOS_FAKE = {
    "result":"success",
 "documentation":"https://www.exchangerate-api.com/docs",
 "terms_of_use":"https://www.exchangerate-api.com/terms",
 "time_last_update_unix":1782259202,
 "time_last_update_utc":"Wed, 24 Jun 2026 00:00:02 +0000",
 "time_next_update_unix":1782345602,
 "time_next_update_utc":"Thu, 25 Jun 2026 00:00:02 +0000",
 "base_code":"BRL",
 "conversion_rates":{
  "BRL":1,
  "AED":0.7099,
  "AFN":12.3908,
  "ALL":16.0292,
  "AMD":71.5841,
  "ANG":0.3460,
  "AOA":182.1700,
  "ARS":284.1265,
  "AUD":0.2789,
  "AWG":0.3460,
  "AZN":0.3300,
  "BAM":0.3319,
  "BBD":0.3866,
  "BDT":23.7406,
  "BGN":0.3319,
  "BHD":0.07268,
  "BIF":580.6311,
  "BMD":0.1933,
  "BND":0.2504,
  "BOB":1.3407,
  "BSD":0.1933,
  "BTN":18.2964,
  "BWP":2.6657,
  "BYN":0.5450,
  "BZD":0.3866,
  "CAD":0.2742,
  "CDF":446.3060,
  "CHF":0.1564,
  "CLF":0.004450,
  "CLP":175.8781,
  "CNH":1.3114,
  "CNY":1.3184,
  "COP":664.6404,
  "CRC":88.0635,
  "CUP":4.6391,
  "CVE":18.7122,
  "CZK":4.1073,
  "DJF":34.3525,
  "DKK":1.2660,
  "DOP":11.3454,
  "DZD":25.8831,
  "EGP":9.6120,
  "ERN":2.8994,
  "ETB":31.0837,
  "EUR":0.1697,
  "FJD":0.4356,
  "FKP":0.1463,
  "FOK":1.2660,
  "GBP":0.1463,
  "GEL":0.5148,
  "GGP":0.1463,
  "GHS":2.1761,
  "GIP":0.1463,
  "GMD":14.3782,
  "GNF":1700.2985,
  "GTQ":1.4790,
  "GYD":40.6837,
  "HKD":1.5145,
  "HNL":5.1827,
  "HRK":1.2786,
  "HTG":25.4165,
  "HUF":60.2604,
  "IDR":3445.7311,
  "ILS":0.5789,
  "IMP":0.1463,
  "INR":18.2986,
  "IQD":254.4894,
  "IRR":266839.3782,
  "ISK":24.4830,
  "JEP":0.1463,
  "JMD":30.6304,
  "JOD":0.1370,
  "JPY":31.2139,
  "KES":25.0843,
  "KGS":17.0067,
  "KHR":786.9079,
  "KID":0.2788,
  "KMF":83.4880,
  "KRW":296.3551,
  "KWD":0.05993,
  "KYD":0.1611,
  "KZT":94.1947,
  "LAK":4276.6822,
  "LBP":17299.8724,
  "LKR":64.8007,
  "LRD":35.3184,
  "LSL":3.1898,
  "LYD":1.2467,
  "MAD":1.8141,
  "MDL":3.4105,
  "MGA":830.6250,
  "MKD":10.4037,
  "MMK":407.6795,
  "MNT":689.3372,
  "MOP":1.5599,
  "MRU":7.7932,
  "MUR":9.3030,
  "MVR":2.9978,
  "MWK":338.1969,
  "MXN":3.3829,
  "MYR":0.7997,
  "MZN":12.3606,
  "NAD":3.1898,
  "NGN":264.7373,
  "NIO":7.1352,
  "NOK":1.8898,
  "NPR":29.2742,
  "NZD":0.3405,
  "OMR":0.07432,
  "PAB":0.1933,
  "PEN":0.6564,
  "PGK":0.8498,
  "PHP":11.8074,
  "PKR":53.7892,
  "PLN":0.7264,
  "PYG":1179.7721,
  "QAR":0.7036,
  "RON":0.8913,
  "RSD":19.9627,
  "RUB":14.4281,
  "RWF":284.4957,
  "SAR":0.7249,
  "SBD":1.5591,
  "SCR":2.8604,
  "SDG":86.9259,
  "SEK":1.8780,
  "SGD":0.2504,
  "SHP":0.1463,
  "SLE":4.8597,
  "SLL":4859.7110,
  "SOS":111.1617,
  "SRD":7.2960,
  "SSP":1002.4637,
  "STN":4.1577,
  "SYP":21.7807,
  "SZL":3.1898,
  "THB":6.4184,
  "TJS":1.8001,
  "TMT":0.6807,
  "TND":0.5698,
  "TOP":0.4658,
  "TRY":8.9763,
  "TTD":1.3150,
  "TVD":0.2788,
  "TWD":6.1157,
  "TZS":510.9282,
  "UAH":8.7262,
  "UGX":712.5926,
  "USD":0.1933,
  "UYU":7.7656,
  "UZS":2322.3230,
  "VES":120.1388,
  "VND":5069.6948,
  "VUV":22.9900,
  "WST":0.5329,
  "XAF":111.3173,
  "XCD":0.5219,
  "XCG":0.3460,
  "XDR":0.1437,
  "XOF":111.3173,
  "XPF":20.2509,
  "YER":46.2131,
  "ZAR":3.1897,
  "ZMW":3.4680,
  "ZWG":5.1813,
  "ZWL":5.1813
 }
}


def test_filtrar_moedas_retorno_10_registros():
    resultado = filtrar_moedas(DADOS_FAKE)
    assert len(resultado) == 10


def test_filtrar_moedas_campos_corretos():
    resultado = filtrar_moedas(DADOS_FAKE)
    primeiro = resultado[0]
    assert "moeda" in primeiro
    assert "cotacao_brl" in primeiro
    assert "timestamp_coleta" in primeiro
    assert "timestamp_api" in primeiro
    assert "timestamp_nextattapi" in primeiro

def test_filtrar_moedas_corretas():
    resultado = filtrar_moedas(DADOS_FAKE)
    moedas_retornadas = [r["moeda"] for r in resultado]
    assert "USD" in moedas_retornadas
    assert "EUR" in moedas_retornadas
    assert "BRL" not in moedas_retornadas
    assert "ARS" not in moedas_retornadas


def test_get_secret_retorna_api_key():
    with patch("extract.boto3.client") as mock_client:
        mock_client.return_value.get_secret_value.return_value = {
            "SecretString": '{"api_key": "chave-fake-123"}'
        }
        from extract import get_secret
        resultado = get_secret("forex-pipeline/api-key")
        assert resultado["api_key"] == "chave-fake-123"


def test_validar_registros_volume_minimo():
    registros_incompletos = [
        {"moeda": "USD", "cotacao_brl": 0.19, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "EUR", "cotacao_brl": 0.17, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
    ]
    with pytest.raises(ValueError):
        validar_registros(registros_incompletos)

def test_validar_registros_cotacao_invalida():
    registros = [
        {"moeda": "USD", "cotacao_brl": 0, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "EUR", "cotacao_brl": 0.17, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "JPY", "cotacao_brl": 31.2, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "GBP", "cotacao_brl": 0.14, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "AUD", "cotacao_brl": 0.27, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CAD", "cotacao_brl": 0.27, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CHF", "cotacao_brl": 0.15, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CNY", "cotacao_brl": 1.31, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "HKD", "cotacao_brl": 1.51, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "SEK", "cotacao_brl": 1.87, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
    ]
    with pytest.raises(ValueError):
        validar_registros(registros)


def test_validar_registros_timestamp_vazio():
    registros = [
        {"moeda": "USD", "cotacao_brl": 0.19, "timestamp_api": "", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "EUR", "cotacao_brl": 0.17, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "JPY", "cotacao_brl": 31.2, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "GBP", "cotacao_brl": 0.14, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "AUD", "cotacao_brl": 0.27, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CAD", "cotacao_brl": 0.27, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CHF", "cotacao_brl": 0.15, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CNY", "cotacao_brl": 1.31, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "HKD", "cotacao_brl": 1.51, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "SEK", "cotacao_brl": 1.87, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
    ]
    with pytest.raises(ValueError):
        validar_registros(registros)

def test_validar_registros_moeda_duplicada():
    registros = [
        {"moeda": "USD", "cotacao_brl": 0.19, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "USD", "cotacao_brl": 0.19, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "JPY", "cotacao_brl": 31.2, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "GBP", "cotacao_brl": 0.14, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "AUD", "cotacao_brl": 0.27, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CAD", "cotacao_brl": 0.27, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CHF", "cotacao_brl": 0.15, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "CNY", "cotacao_brl": 1.31, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "HKD", "cotacao_brl": 1.51, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
        {"moeda": "SEK", "cotacao_brl": 1.87, "timestamp_api": "Wed, 24 Jun 2026", "timestamp_nextattapi": "Thu, 25 Jun 2026"},
    ]
    with pytest.raises(ValueError):
        validar_registros(registros)