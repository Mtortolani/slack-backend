from random import random
from operator import __add__

from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

class SparkQuery:
    def __init__(self, database: str = 'slack_database', col: str = 'user_col'):
    #set directory
        self.mongo_url = 'mongodb://localhost:27017/'
        self.database = 'slack_database'
        self.col = 'user_col'

        # establish spark session
        # NOTE:'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1.jar' may need to be downloaded from online and placed in $SPARK_HOME$/jars
        self.spark = SparkSession\
            .builder\
                .master('local')\
                    .appName('slackApp')\
                        .config("spark.mongodb.input.uri", self.mongo_url + self.database +'.'+ self.col)\
                            .config("spark.mongodb.output.uri", self.mongo_url + self.database +'.'+ self.col)\
                                .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
                                    .getOrCreate()
                        
        self.sqlC = SQLContext(self.spark)
    def checkSchema(self):
        # print out schema format for current collection
        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
        df.printSchema()
    
    def showAllData(self):
        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('user_col')
        df =self.sqlC.sql('SELECT * FROM user_col')
        df.show()

    def randomUserIds(self,count:int = 1) -> list:
        # utilize SQLContext to run sql queries on mongo df
        # run generic pull all query
        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('user_col')
        df = self.sqlC.sql(f'''SELECT user_id FROM user_col
                    Order By RAND()
                    LIMIT {count}''')
        df.show()
        user_id = [id for id in df.collect()[0]]
        return user_id

def main():
    SQ = SparkQuery('slack_database','user_col')
    SQ.checkSchema()
    print(SQ.randomUserIds())
    

if __name__ == '__main__':
    main()

# ORDER BY RAND()
# LIMIT 1

# data = sqlC.read.format('com.mongodb.spark.sql.DefaultSource').option('uri', mongo_ip + 'col').load()
# data.createOrReplaceTempView('col')
# data = sqlC.sql('SELECT * FROM col')
# data.show()
# df = spark.read.format('mongodb').load()
# df.printSchema()