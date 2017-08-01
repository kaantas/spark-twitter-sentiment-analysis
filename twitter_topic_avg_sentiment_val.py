from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import json
import sys
from pyspark.sql.types import *

def fun(avg_senti_val):
	try:
		if avg_senti_val < 0: return 'NEGATIVE'
		elif avg_senti_val == 0: return 'NEUTRAL'
		else: return 'POSITIVE'
	except TypeError:
		return 'NEUTRAL'

if __name__ == "__main__":

	schema = StructType([                                                                                          
		StructField("text", StringType(), True),
		StructField("senti_val", DoubleType(), True)    
	])
    
	spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()

	kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "twitter").load()

	kafka_df_string = kafka_df.selectExpr("CAST(value AS STRING)")

	tweets_table = kafka_df_string.select(from_json(col("value"), schema).alias("data")).select("data.*")

	sum_val_table = tweets_table.select(avg('senti_val').alias('avg_senti_val'))
	
	# udf = USER DEFINED FUNCTION
	udf_avg_to_status = udf(fun, StringType())

	# avarage of senti_val column to status column
	new_df = sum_val_table.withColumn("status", udf_avg_to_status("avg_senti_val"))

	query = new_df.writeStream.outputMode("complete").format("console").start()

	query.awaitTermination()

