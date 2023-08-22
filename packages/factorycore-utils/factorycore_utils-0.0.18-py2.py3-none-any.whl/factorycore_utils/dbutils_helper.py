def get_dbutils(spark):
    from pyspark.dbutils import DBUtils
    return DBUtils(spark)