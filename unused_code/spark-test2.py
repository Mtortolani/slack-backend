import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
print(pyspark.__version__)

conf = pyspark.SparkConf().set('spark.jars.packages',
                            'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
                                .setMaster('local')\
                                    .setAppName('testApp')\
                                        .setAll([('spark.driver.memory', '4g'), 
                                                 ('spark.executor.memory', '5g')])
sc = SparkContext(conf=conf)
sqlC= SQLContext(sc)

mongo_ip = 'mongodb://localhost:27017/test.'
data = sqlC.read.format('com.mongodb.spark.sql.DefaultSource').option('uri', mongo_ip + 'col').load()
data.createOrReplaceTempView('col')
data = sqlC.sql('SELECT * FROM col')
data.show()