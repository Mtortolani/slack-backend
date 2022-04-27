from spark_queries import SparkQuery
from mongo_queries import MongoSearch
from profiler import Profiler
import matplotlib.pyplot as plt
import json

def main():
    MQ = MongoSearch()
    SQ = SparkQuery()
    PF = Profiler()

    # Random arrays function arguments
    user_ids = MQ.randomUsersIds(10)
    workspaceIds = MQ.randomWorkspaceIds(10)

    data_dict = {}
    data_dict['randomUsersIds'] = PF.collect_performance_data_fixed_iters(MQ.randomUsersIds, SQ.randomUsersIds)
    print(f'randomUsersIds completed')
    data_dict['randomWorkspaceIds'] = PF.collect_performance_data_fixed_iters(MQ.randomWorkspaceIds, SQ.randomWorkspaceIds)
    print(f'randomWorkspaceIds completed')
    data_dict['workspaceByUser'] = PF.collect_performance_data_fixed_iters(lambda: MQ.workspaceByUser(user_ids[0]), lambda: SQ.workspaceByUser(user_ids[0]))
    print(f'workspaceByUser completed')
    data_dict['dirChannelMessages'] = PF.collect_performance_data_fixed_iters(lambda: MQ.dirChannelMessages(user_ids[0], user_ids[1]), lambda: SQ.dirChannelMessages(user_ids[0], user_ids[1]))
    print(f'dirChannelMessages completed')
    # TODO: Fix functions, mongo and spark versions return different things
    data_dict['usersInWorkspace'] = PF.collect_performance_data_fixed_iters(lambda: MQ.usersInWorkspace(workspaceIds[0]), lambda: SQ.usersInWorkspace(workspaceIds[0]))
    print(f'usersInWorkspace completed')
    data_dict['channelNamesInWorkspace'] = PF.collect_performance_data_fixed_iters(lambda: MQ.channelNamesInWorkspace(workspaceIds[0]), lambda: SQ.channelNamesInWorkspace(workspaceIds[0]))
    print(f'channelNamesInWorkspace completed')


    # Directly from dictionary
    with open('src\data\profiler_data.json', 'w') as outfile:
        json.dump(data_dict, outfile)

if __name__ == '__main__':
    main()
    
