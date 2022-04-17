from random import random
from operator import __add__

from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
from mongo_queries import workspaceByUser

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
    
    # utilize SQLContext to run sql queries on mongo df
    # run generic pull all query
    def showAllData(self):
        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('user_col')
        df =self.sqlC.sql('SELECT * FROM user_col')
        df.show()

    def randomUserIds(self, count:int = 1) -> list:
        # pick a random user(s)
        df = self.spark.read\
            .option("database", self.database)\
                .option("collection", "user_col")\
                    .format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('user_col')
        df = self.sqlC.sql(f'''SELECT user_id FROM user_col
                    Order By RAND()
                    LIMIT {count}''')
        user_id = [df.collect()[i][0] for i in range(df.count())]
        return user_id
    
    # find all workspaces a user is in
    def workspaceByUser(self, user_id: int) -> list:
        df = self.spark.read\
                .option("database", self.database)\
                    .option("collection", "workspace_col")\
                        .format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('workspace_col')
        df = self.sqlC.sql(f'''select * from workspace_col 
                           where array_contains(members, {user_id})''')
        df.show()
        workspace_ids = []
        for row in df.collect():
            workspace_ids.append(row[0][0])
        return workspace_ids


    # find all messages in direct channel between two users
    # will return empty list if no direct channel between two users exists
    def dirChannelMessages(self, user_id_1: int, user_id_2: int):
        df = self.spark.read\
                .option("database", self.database)\
                    .option("collection", "direct_col")\
                        .format("com.mongodb.spark.sql.DefaultSource").load()
        df = self.sqlC.sql(f'''select * from direct_col 
                           where array_contains(members, {user_id_1})
                           AND array_contains(members, {user_id_2}''')
        df.filter(array_contains('member_ids',[user_id_1,user_id_2])) 
                       
def main():
    SQ = SparkQuery('slack_database','user_col')
    SQ.checkSchema()
    randomId = SQ.randomUserIds(10)
    print(randomId)
    workspacesForUser = SQ.workspaceByUser(randomId[0])
    print(workspacesForUser)
    dir_channels = SQ.dirChannelMessages(randomId[0], randomId[1])

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