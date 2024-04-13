from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder \
    .appName("books") \
    .getOrCreate()

# READ
df = spark.read.format("mongo") \
    .option("uri", "mongodb://192.168.1.16:27017/test.books") \
    .load()

# ADD TIMESTAMP
df = df.withColumn("uploaddate", current_timestamp())

# WRITE
server_target = "192.168.1.16:5432"
db_target = "internal"
user_target = "postgres"
password_target = "postgres"
url_target = "jdbc:postgresql://" + server_target + "/" + db_target
table_target = "raw.books"
mode_write = 'overwrite' # append, overwrite, default 

df.write.format("jdbc") \
    .option("url", url_target) \
    .option("dbtable", table_target) \
    .option("user", user_target) \
    .option("password", password_target) \
    .mode(mode_write) \
    .save()

spark.stop()