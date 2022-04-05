# channel settings: censored words, 
class ChannelSetting:
  def __init__(self, censored_words: list = None, archive: bool = True):
    self.censored_words = set()
    self.archive = False
    
    
#  user settings: language, notifications   
class UserSetting:
  def __init__(self, language: str= 'English', notifications: bool = "None", time_zone: str = 'EST'):
    self.notifications = notifications
    self.language = language
    self.time_zone = time_zone