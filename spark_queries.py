from random import random
from operator import __add__

from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *


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
        # self.spark.conf.set("spark.executor.memory", "2g")
        # self.spark.conf.set("spark.executor.cores", "2")
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
        
    # pick a random user(s)
    def randomUsersIds(self, count:int = 1) -> list:
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
    
    # pick a random workspace(s)
    def randomWorkspaceIds(self, count:int = 1) -> list:
        df = self.spark.read\
            .option("database", self.database)\
                .option("collection", "workspace_col")\
                    .format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('workspace_col')
        df = self.sqlC.sql(f'''SELECT _id FROM workspace_col
                    Order By RAND()
                    LIMIT {count}''')
        workspace_id = [df.collect()[i][0][0] for i in range(df.count())]
        return workspace_id
    
    # find all workspaces a user is in
    def workspaceByUser(self, user_id: int) -> list:
        df = self.spark.read\
                .option("database", self.database)\
                    .option("collection", "workspace_col")\
                        .format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('workspace_col')
        df = self.sqlC.sql(f'''select * from workspace_col 
                           where array_contains(members, {user_id})''')
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
        df.createOrReplaceTempView('direct_col')
        df = self.sqlC.sql(f'''select _id from direct_col 
                           where array_contains(member_ids, {user_id_1})
                           AND array_contains(member_ids, {user_id_2})''')
        dir_workspace_ids = []
        for row in df.collect():
            dir_workspace_ids.append(row[0])
        return dir_workspace_ids
    
    # find all user ids in a workspace
    # TODO: make the same as mongo version, return username instead of id
    def usersInWorkspace(self, workspace_id)->list:
        df = self.spark.read\
                .option("database", self.database)\
                    .option("collection", "workspace_col")\
                        .format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('workspace_col')
        df = self.sqlC.sql(f"""select members from workspace_col 
                           where _id.oid = '{workspace_id}'""")
        dir_member_ids = df.collect()[0][0]
        return dir_member_ids
    
    # find names of all available channels in workspace
    def channelNamesInWorkspace(self, workspace_id)->list:
        df = self.spark.read\
                .option("database", self.database)\
                    .option("collection", "workspace_col")\
                        .format("com.mongodb.spark.sql.DefaultSource").load()
        df.createOrReplaceTempView('workspace_col')
        df = self.sqlC.sql(f"""select channels from workspace_col 
                           where _id.oid = '{workspace_id}'""")
        channel_names = [name for name, messages in df.collect()[0][0].items()]
        return channel_names

                       
def main():
    SQ = SparkQuery('slack_database','user_col')
    SQ.checkSchema()
    userIds = SQ.randomUsersIds(10)
    print(userIds)
    print(SQ.workspaceByUser(userIds[0]))
    print(SQ.dirChannelMessages(userIds[0], userIds[1]))
    workspaceIds = SQ.randomWorkspaceIds(10)
    print(SQ.usersInWorkspace(workspaceIds[0]))
    print(SQ.channelNamesInWorkspace(workspaceIds[0]))

if __name__ == '__main__':
    main()
