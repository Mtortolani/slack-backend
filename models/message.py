# as inspired by the discord database
# https://blog.discord.com/how-discord-stores-billions-of-messages-7fa6ec7ee4c7

class Message:
    def __init__(self, content, author_id: str = None, channel_id: str = None):
        #PK
        self.message_id = None
        #FK
        self.author_id = author_id 
        self.channel_id = channel_id
        #Attributes
        self.content = content
    

    def __str__(self):
        return str(self.content)
    
    #id
    def getId(self):
        return self.message_id
    #author_id
    def getAuthorId(self):
        return self.author_id
    #channel_id
    def getChanneId(self):
        return self.channel_id
    #content
    def getContent(self):
        return self.content
    def setContent(self, content):
        self.content = content
    
    
    
    
    
