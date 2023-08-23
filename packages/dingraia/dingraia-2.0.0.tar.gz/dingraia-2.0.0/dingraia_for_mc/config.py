from typing import Union, List


class AES_KEY:
    type: str
    string = ""
    
    def __init__(self, Aes_Key):
        self.string = Aes_Key
    
    def __str__(self):
        return self.string
    
    
class Token:
    type: str
    string = ""
    
    def __init__(self, token):
        self.string = token
    
    def __str__(self):
        return self.string
    
    
class CropID:
    type: str
    string = ""
    
    def __init__(self, crop_id):
        self.string = crop_id
    
    def __str__(self):
        return self.string
    
    
class Group_Webhook:
    
    def __init__(self, Access_Token: str, Secure_Key: str, GroupID: str = None):
        self.Access_Token = Access_Token
        self.Secure_Key = Secure_Key
        self.GroupID = GroupID[GroupID.rfind('$'):] if GroupID is not None else None
        if self.GroupID:
            if len(self.GroupID) < 2:
                raise ValueError("不正确的群ID！请从回调中提取conversationid！")
        

class Config:
    
    def __init__(self,
                 event_callbacks: List[list[Union[str, AES_KEY], Union[str, Token], Union[str, CropID]]] = None,
                 group_webhooks: List[Group_Webhook] = None
                 ):
        self.event_callbacks = [[str(y) for y in x] for x in event_callbacks] if event_callbacks is not None else None
        self.group_webhooks = group_webhooks
    
    
