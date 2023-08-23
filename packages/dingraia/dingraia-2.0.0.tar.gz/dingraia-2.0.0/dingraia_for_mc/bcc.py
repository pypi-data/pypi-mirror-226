import json
from .signer import sign_js, decrypt
from flask import request
from .DingTalk import Dingtalk
from .model import Group, Member, Bot
from .event import MessageEvent
from .message.chain import MessageChain
from .saya import Channel
from .event.message import *
from loguru import logger
from .tools.debug import delog
channel = Channel.current()
callbacks = []


@logger.catch
async def bcc():
    res = request.get_json()
    delog.info(json.dumps(res, indent=2, ensure_ascii=False), no=50)
    _e = dispackage(res)
    if _e.get('success'):
        if isinstance(_e.get('event_type'), BasicMessage):
            log(_e.get('send_data'))
        await channel.radio(_e.get('event_type'), *_e.get('send_data'))
    if not _e:
        logger.warning("无法解包！")
        return ""
    return _e.get('returns') or {'err': 0}


@logger.catch
def dispackage(data: dict) -> dict:
    if "conversationType" in data:
        conversationtype = data.get("conversationType")
        if conversationtype is not None:
            bot = Bot(origin=data)
            group = Group(origin=data)
            member = Member(origin=data)
            if conversationtype == "2":
                at_users = [userid.get("dingtalkId") for userid in data.get("atUsers") if userid.get("dingtalkId")[userid.get("dingtalkId").rfind('$'):] != bot.origin_id]
            else:
                at_users = []
            if data.get('msgtype') != 'text':
                raise ValueError("不支持解析文本以外的消息")
            mes = data.get('text').get('content')
            for _ in mes:
                if mes.startswith(" "):
                    mes = mes[1:]
                else:
                    break
            # logger.info(at_users)
            message = MessageChain(mes, at=at_users)
            event = MessageEvent(data.get('msgtype'), data.get('msgId'), data.get('isInAtList'), message, group, member)
            return {
                "success": True,
                "send_data": [group, member, message, event, bot],
                "event_type": GroupMessage,
                "returns": ""
            }
        else:
            logger.error("不支持的对话类型")
            logger.error(json.dumps(data, indent=2, ensure_ascii=False))
            return {
                "success": False,
                "send_data" : [],
                "event_type": None,
                "returns"   : ""
            }
    elif "encrypt" in data:
        app = Dingtalk()
        if app.config is not None:
            _e = None
            for call in app.config.event_callbacks:
                try:
                    _e = decrypt(data.get("encrypt"), call[0])
                except json.JSONDecodeError:
                    continue
                else:
                    break
            if _e is None:
                logger.error("无法解密，请检查配置的事件回调密钥")
                return {
                    "success"   : False,
                    "send_data" : [],
                    "event_type": None,
                    "returns"   : ""
                }
            if type(_e) == dict:
                logger.info(_e)
                return {
                    "success"   : True,
                    "send_data" : [],
                    "event_type": None,
                    "returns"   : sign_js(call[1], call[0], call[2])
                }
            return {
                "success"   : False,
                "send_data" : [],
                "event_type": None,
                "returns"   : ""
            }
        return {
            "success"   : False,
            "send_data" : [],
            "event_type": None,
            "returns"   : ""
        }
    else:
        logger.error(f"未知的回调类型:{json.dumps(data, indent=2, ensure_ascii=False)}")
        return {
            "success"   : False,
            "send_data" : [],
            "event_type": None,
            "returns"   : ""
        }
        


def log(data):
    if data[0].name is None:
        data[0].name = "临时会话"
    Dingtalk.log.info(f"[RECV][{data[0].name}({int(data[0])})][{data[1].name}({int(data[1])})] -> {str(data[2])}")
    
    

