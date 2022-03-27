# slack-backend
DS4300 Final Project

Replicating Slack’s backend data architecture and basic functionalities with AWS Cloud, NoSQL, and Distributed Computing technologies.

## Redis Data Structure
<b>Users</b>: key = user_{id} -> value = hashmap: {dms: [list of user ids], workspaces: [list of workspace ids]}, Ex. user_1 -> {dms: [2,3], workspaces: [10,14]} <br>
<b>Direct Channels</b>: key = dc_{smaller user id}_{larger user id} -> value = [list of message ids], Ex. dc_1_2 -> [1,6,29]<br>
<b>Messages</b>: key = m_{id}_{user/sender id} -> value = message string, Ex. m_3_5 -> "Hello World" <br>
<b>Workspaces</b>: key = workspace_{id} -> value = hashmap: {users: [list of user ids], channels: [list of channel ids]}, Ex. workspace_17 -> {users: [1,2,3,6], channels: [4,16,19,100]}<br>
<b>Channels</b>: key = channel_{id} -> value = hashmap: {users: [list of user ids], messages: [list of message ids]}, Ex. channel_19 -> {users: [1,3], messages: [300,423]}

## Resources
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html

## Tips
Cmd + Shift + V to preview Markdown File