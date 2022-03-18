from models import Message, Workspace

M1 = Message('message content', 'author_id', 'channel_id')
print(M1)
print(M1.message_id)

W1 = Workspace('Workspace 1 Title')