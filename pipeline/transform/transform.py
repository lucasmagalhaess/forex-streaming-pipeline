import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, round as spark_round,
    current_timestamp, to_date,
    explode, avg, stddev, count
)
from pyspark.sql.functions import max as spark_max, min as spark_min


BUCKET = "forex-streaming-datalake-dev"


def criar_spark():
    return SparkSession.builder \
        .appName("forex-transform") \
        .getOrCreate()


def transform_silver(spark, bronze_path, silver_path):
    print(f"📥 Lendo Bronze: {bronze_path}")
    df_raw = spark.read.option("multiline", "true").json(bronze_path)
    df = df_raw.select(explode("registros").alias("registro"))
    df = df.select(
        col("registro.moeda").alias("moeda"),
        col("registro.cotacao_brl").cast("double").alias("cotacao_brl"),
        col("registro.timestamp_coleta").alias("timestamp_coleta"),
        col("registro.timestamp_api").alias("timestamp_api"),
        col("registro.timestamp_nextattapi").alias("timestamp_nextattapi")
    )
    df_silver = df \
        .filter(col("moeda").isNotNull()) \
        .filter(col("cotacao_brl").isNotNull()) \
        .filter(col("cotacao_brl") > 0) \
        .dropDuplicates(["moeda"]) \
        .withColumn("cotacao_usd", spark_round(col("cotacao_brl") / 0.1933, 4)) \
        .withColumn("data_extracao", to_date(col("timestamp_coleta"))) \
        .withColumn("processado_em", current_timestamp())
    print(f"✅ Silver: {df_silver.count()} registros")
    df_silver.write.mode("overwrite").partitionBy("data_extracao").parquet(silver_path)
    print(f"✅ Silver salva: {silver_path}")


def transform_gold_bi(spark, silver_path, gold_bi_path):
    df_silver = spark.read.parquet(silver_path)
    df_gold_bi = df_silver \
        .groupBy("moeda") \
        .agg(
            spark_max("cotacao_brl").alias("cotacao_brl_atual"),
            spark_max("cotacao_usd").alias("cotacao_usd_atual"),
            avg("cotacao_brl").alias("media_cotacao_brl"),
            spark_max("timestamp_api").alias("ultima_atualizacao_api"),
            spark_max("data_extracao").alias("data_extracao")
        ) \
        .withColumn("classificacao",
            when(col("cotacao_brl_atual") < 0.5, "moeda_forte")
            .when(col("cotacao_brl_atual") < 1.0, "moeda_media")
            .otherwise("moeda_fraca")
        ) \
        .withColumn("processado_em", current_timestamp())
    print(f"✅ Gold BI: {df_gold_bi.count()} moedas")
    df_gold_bi.write.mode("overwrite").parquet(gold_bi_path)
    print(f"✅ Gold BI salva: {gold_bi_path}")


def transform_gold_ml(spark, silver_path, gold_ml_path):
    df_silver = spark.read.parquet(silver_path)
    df_gold_ml = df_silver \
        .groupBy("moeda") \
        .agg(
            spark_max("cotacao_brl").alias("cotacao_brl_atual"),
            avg("cotacao_brl").alias("media_cotacao_brl"),
            spark_min("cotacao_brl").alias("min_cotacao_brl"),
            spark_max("cotacao_brl").alias("max_cotacao_brl"),
            stddev("cotacao_brl").alias("desvio_padrao_cotacao"),
            count("moeda").alias("total_registros"),
            spark_max("cotacao_usd").alias("cotacao_usd_atual"),
            spark_max("data_extracao").alias("ultima_data_extracao")
        ) \
        .withColumn("amplitude",
            spark_round(col("max_cotacao_brl") - col("min_cotacao_brl"), 6)
        ) \
        .withColumn("processado_em", current_timestamp())
    print(f"✅ Gold ML: {df_gold_ml.count()} features")
    df_gold_ml.write.mode("overwrite").parquet(gold_ml_path)
    print(f"✅ Gold ML salva: {gold_ml_path}")


if __name__ == "__main__":
    bronze = f"s3://{BUCKET}/bronze/forex/data=2026-06-24/"
    silver = f"s3://{BUCKET}/silver/forex/"
    gold_bi = f"s3://{BUCKET}/gold/bi/forex/"
    gold_ml = f"s3://{BUCKET}/gold/ml/forex/"

    spark = criar_spark()
    spark.sparkContext.setLogLevel("WARN")

    transform_silver(spark, bronze, silver)
    transform_gold_bi(spark, silver, gold_bi)
    transform_gold_ml(spark, silver, gold_ml)

    spark.stop()