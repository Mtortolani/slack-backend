from spark_queries import SparkQuery
from mongo_queries import MongoSearch
from profiler import Profiler
import matplotlib.pyplot as plt

MQ = MongoSearch()
SQ = SparkQuery()
PF = Profiler()

# Random arrays function arguments
user_ids = MQ.randomUsersIds(10)
workspaceIds = MQ.randomWorkspaceIds(10)

data_randomUsersIds = PF.collect_performance_data_fixed_iters(MQ.randomUsersIds, SQ.randomUsersIds)
print(1)
data_randomWorkspaceIds = PF.collect_performance_data_fixed_iters(MQ.randomWorkspaceIds, SQ.randomWorkspaceIds)
print(2)
data_workspaceByUser = PF.collect_performance_data_fixed_iters(lambda: MQ.workspaceByUser(user_ids[0]), lambda: SQ.workspaceByUser(user_ids[0]))
print(3)
data_dirChannelMessages = PF.collect_performance_data_fixed_iters(lambda: MQ.dirChannelMessages(user_ids[0], user_ids[1]), lambda: SQ.dirChannelMessages(user_ids[0], user_ids[1]))
print(4)
# TODO: Fix functions, mongo and spark versions return different things
data_usersInWorkspace = PF.collect_performance_data_fixed_iters(lambda: MQ.usersInWorkspace(workspaceIds[0]), lambda: SQ.usersInWorkspace(workspaceIds[0]))
print(5)
data_channelNamesInWorkspace = PF.collect_performance_data_fixed_iters(lambda: MQ.channelNamesInWorkspace(workspaceIds[0]), lambda: SQ.channelNamesInWorkspace(workspaceIds[0]))
print(6)
print(data_channelNamesInWorkspace)