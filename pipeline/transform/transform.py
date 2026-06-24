import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, round as spark_round,
    current_timestamp, to_date, lit
)


MOEDAS = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "SEK"]
BUCKET = "forex-streaming-datalake-dev"


def criar_spark():
    return SparkSession.builder \
        .appName("forex-transform-silver") \
        .getOrCreate()


def classificar_variacao(variacao_col):
    return when(variacao_col > 5, "alta") \
           .when(variacao_col > 0, "leve_alta") \
           .when(variacao_col == 0, "estavel") \
           .when(variacao_col > -5, "leve_baixa") \
           .otherwise("baixa")


def transform(bronze_path, silver_path):
    spark = criar_spark()
    spark.sparkContext.setLogLevel("WARN")

    print(f"📥 Lendo Bronze: {bronze_path}")
    df_raw = spark.read.option("multiline", "true").json(bronze_path)

    from pyspark.sql.functions import explode
    df = df_raw.select(explode("registros").alias("registro"))

    df = df.select(
        col("registro.moeda").alias("moeda"),
        col("registro.cotacao_brl").cast("double").alias("cotacao_brl"),
        col("registro.timestamp_coleta").alias("timestamp_coleta"),
        col("registro.timestamp_api").alias("timestamp_api"),
        col("registro.timestamp_nextattapi").alias("timestamp_nextattapi")
    )

    print(f"📊 Total de registros lidos: {df.count()}")

    # Limpeza
    df_silver = df \
        .filter(col("moeda").isNotNull()) \
        .filter(col("cotacao_brl").isNotNull()) \
        .filter(col("cotacao_brl") > 0) \
        .dropDuplicates(["moeda"])

    # Regras de negócio por linha
    df_silver = df_silver \
        .withColumn("cotacao_usd",
            spark_round(col("cotacao_brl") / 0.1933, 4)) \
        .withColumn("data_extracao",
            to_date(col("timestamp_coleta"))) \
        .withColumn("processado_em", current_timestamp())

    print(f"✅ Silver transformada: {df_silver.count()} registros")
    df_silver.show(truncate=False)

    df_silver.write \
        .mode("overwrite") \
        .partitionBy("data_extracao") \
        .parquet(silver_path)

    print(f"✅ Silver salva: {silver_path}")
    spark.stop()


if __name__ == "__main__":
    bronze = sys.argv[1] if len(sys.argv) > 1 else \
        f"s3://{BUCKET}/bronze/forex/data=2026-06-24/"
    silver = sys.argv[2] if len(sys.argv) > 2 else \
        f"s3://{BUCKET}/silver/forex/"
    transform(bronze, silver)