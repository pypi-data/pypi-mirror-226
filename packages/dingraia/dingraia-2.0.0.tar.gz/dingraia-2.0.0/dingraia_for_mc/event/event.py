from dingraia.model import *


class BasicEvent:
    
    type = "BasicEvent"
    
    
class CheckUrl(BasicEvent):
    
    type = 'CheckUrl'
    
    
class CheckIn(BasicEvent):
    
    type = "CheckIn"
    
    member: Member
    
    bot: Bot
    