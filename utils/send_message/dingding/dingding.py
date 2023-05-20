#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.send_message.dingding.dingding_config import BUG_ROBOT
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse


class DingDingRobot:
    """
    access_token:机器人access_token
    secret: 密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串，例如：SECxxxxxxxx
    msg:通知内容
    """

    def get_user_id(self, at_user):
        params = {
            "email": at_user + "@haohaozhu.com"
        }
        req = requests.get("https://dingtalk-account-callback.haohaozhu.cn/getDingTalkIdByEmail", params=params)

        userid = json.loads(req.text).get("ding_talk_id")
        # print("userid是========", userid)

        return userid

    def add_timestamp_sign(self, access_token, secret):
        # 加签
        timestamp = str(round(time.time() * 1000))
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        dingding_url = "https://oapi.dingtalk.com/robot/send?access_token={0}&timestamp={1}&sign={2}".format(access_token, timestamp, sign)
        return dingding_url

    def send_text_msg(self, access_token, secret, at_user='', msg=None):
        # robot = DingtalkChatbot(webhook=webhook, secret=secret)
        # robot.send_markdown(title=title, text=msg_markdown, is_at_all=True)
        headers = {"Content-Type": "application/json"}
        user_list = at_user.split(',')
        # print(user_list)
        if user_list[0] == '':
            data_json_atall = json.dumps({
                "at": {
                    "isAtAll": "true"
                },
                "text": {
                    "content": msg
                },
                "msgtype": "text"
            })
            res_at_all = requests.post(url=self.add_timestamp_sign(access_token, secret), headers=headers, data=data_json_atall)
        else:
            error = ''
            at_user_ids = []
            content_at_user = ''
            for user in user_list:
                user_id = self.get_user_id(user)
                print("user_id=====", user_id, type(user_id))
                if not user_id:
                   error += "没找到user_id"
                at_user_ids.append(user_id)
                content_at_user += user_id
                # print("@某某人===", content_at_user)
            # print("userids======",at_user_ids)
            data_json_at_user = json.dumps({
                "at": {
                    "atUserIds": at_user_ids,
                    "isAtAll": "false"
                },
                "text": {
                    # "content": msg + content_at_user
                    "content": msg
                },
                "msgtype": "text"
            })
            res_at_user = requests.post(url=self.add_timestamp_sign(access_token, secret), headers=headers, data=data_json_at_user)



if __name__ == "__main__":
    msg = "实际发生的咖啡机大煞风景"
    # DingDingRobot().send_text_msg(access_token=BUG_ROBOT["access_token"], secret=BUG_ROBOT["secret"], msg=msg)
    # DingDingRobot().send_text_msg(access_token=BUG_ROBOT["access_token"], secret=BUG_ROBOT["secret"], at_user="wangjianwei,wanghuan", msg=msg)
    DingDingRobot().send_text_msg(access_token=BUG_ROBOT["access_token"], secret=BUG_ROBOT["secret"], at_user="wangjianweif", msg=msg)