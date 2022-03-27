# slack-backend
DS4300 Final Project

Replicating Slack’s backend data architecture and basic functionalities with AWS Cloud, NoSQL, and Distributed Computing technologies.

## Redis Data Structure
<b>Users</b>: key = user_{id} -> value = hashmap {dms: [list of user ids], workspaces: [list of workspace ids]} <br>
<b>Direct Channels</b>: key = dc_{smaller user id}_{larger user id}, Ex. dc_1_2, -> value = [list of string messages] <br>
<b>Messages</b>: String serialized as: {sender id}_{message}, Ex. "3_Hello World" <br>
<b>Workspaces</b>


## Resources
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html

## Tips
Cmd + Shift + V to preview Markdown File