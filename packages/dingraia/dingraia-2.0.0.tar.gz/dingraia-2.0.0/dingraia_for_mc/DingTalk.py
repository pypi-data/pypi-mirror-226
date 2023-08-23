import hmac
import time
import base64
import urllib.parse
from loguru import logger
from functools import reduce
from .message.chain import MessageChain
from .login import url_res
from .model import Group, Webhook
from .message.element import *
from .saya import Channel, Saya
from .tools.debug import delog
from .config import Config


send_url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}"


class Dingtalk:
    """
    send_message: msg\n
    send_link: title, text, message_url,  picture_url\n
    send_markdown: title, text\n
    send_actioncard: title, text, button, orientation\n
    send_feedcard: links\n
    """
    config: Config = None
    
    @staticmethod
    def __init__(config: Config = None):
        if Dingtalk.config is None:
            Dingtalk.config = config
    
    async def send_message(self, target: Union[Group, str, Webhook, None], msg, header=None):
        """发送普通的文本信息
        
        Args:
            target: 要发送的地址，可以是Group, str格式的链接, 或者None发送到测试群
            msg: 要发送的文本
            header: 要包含的请求头

        Returns:
            List(bool)

        """
        if type(msg) == Link:
            send_data = msg.data
        elif type(msg) == Markdown:
            send_data = msg.data
        elif type(msg) == ActionCard:
            send_data = msg.data
        elif type(msg) == FeedCard:
            send_data = msg.data
        else:
            send_data = {
                "msgtype": "text",
                "text"   : {
                    "content": str(msg)
                }
            }
        if type(msg) == MessageChain:
            if ats := msg.include(At):
                at = reduce(lambda x, y: x + y, ats)
                send_data["at"] = at.data
        if target is None:
            sign = self.get_sign()
            url = send_url.format(sign[2], sign[1], sign[0])
            self.log.info(f"[SEND] <- {repr(str(msg))[1:-1]}")
        elif isinstance(target, Group):
            if time.time() < target.webhook.expired_time:
                url = target.webhook.url
                self.log.info(f"[SEND][{target.name}({int(target)})] <- {repr(str(msg))[1:-1]}")
            else:
                logger.error("群组的Webhook链接已经过期！请检查来源IP是否正确或服务器时钟是否正确")
                return [False, -1]
        elif isinstance(target, Webhook):
            if time.time() < target.expired_time:
                url = target.url
            else:
                logger.error("指定的临时Webhook链接已经过期")
                return
        else:
            url = str(target)
            self.log.info(f"[SEND] <- {repr(str(msg))[1:-1]}")
        delog.info(send_data, no=60)
        return await self._send(url, send_data, header)
    
    @staticmethod
    class log:
        def info(*mes):
            logger.info(*mes)
        
        def debug(*mes):
            logger.debug(*mes)
        
        def warning(*mes):
            logger.warning(*mes)
        
        def success(*mes):
            logger.success(*mes)

    @classmethod
    def get_sign(cls, secure_key: str = None, group=None):
        if secure_key is None:
            if cls.config:
                if cls.config.group_webhooks is not None and cls.config.group_webhooks:
                    if group is None:
                        secure_key = cls.config.group_webhooks[0].Secure_Key
        timestamp = str(round(time.time() * 1000))
        sign_str = timestamp + '\n' + secure_key
        sign = hmac.new(secure_key.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256).digest()
        sign = base64.b64encode(sign)
        sign = urllib.parse.quote_plus(sign)
        return sign, timestamp, secure_key
    
    @staticmethod
    async def _send(url, send_data, header=None):
        delog.info(f"发送中:{url}", no=40)
        if url and "http" not in url:
            url = 'http://' + url
        if not url:
            logger.error("空的返回地址")
            return [False]
        try:
            resp = await url_res(url, method='POST', data=send_data, header=header, res='json')
            delog.success("发送完成")
        except Exception as err:
            logger.exception(f"端口发送失败！", err)
            return [False]
        else:
            delog.info(resp, no=40)
            if not resp['errcode']:
                delog.success(f"成功!", no=40)
                return [True]
            else:
                logger.error(f"发送失败！错误代码：{resp['errcode']}，错误信息：{resp['errmsg']}")
                return [False, resp['errcode'], resp['errmsg']]
            
    def start(self):
        Channel().set_channel()
        Saya().set_channel()
