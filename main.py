from pyspark.sql import *

spark = SparkSession.builder.appName("SparkByExamples.com").master("local[2]").getOrCreate()

data_List = [("James", "", "Smith", "36636", "M", 3000),
                ("Michael", "Rose", "", "40288", "M", 4000),
                ("Robert", "", "Williams", "42114", "", 4000),
                ("Maria", "Anne", "Jones", "39192", "F", 4000),
                ("Jen", "Mary", "Brown", "", "F", -1)]

df = spark.createDataFrame(data_List).toDF("F_NAME","M_NAME","L_NAME","ID_NO","GENDER","SALARY")
df.show()

