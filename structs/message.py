# as inspired by the discord database
# https://blog.discord.com/how-discord-stores-billions-of-messages-7fa6ec7ee4c7

class Message:
    def __init__(self, content, message_id = None, author_id = None, channel_id=None):
        self.content = content
        self.message_id = message_id
        self.author_id = author_id
        self.channel_id = channel_id
        
    def __str__(self):
        return str(self.content)
