"""公共方法"""
import json
import os
import re

from core.mongo_client import MongoClient
from env import env_app


class PublicFun(object):

    @staticmethod
    def handle_data(data):
        msg_type = False
        try:
            if isinstance(data['data'], dict):
                msg_type = data['data'].get('msgtype') in [0, 2]
                if data['data'].get('content'):
                    data['data']['content'] = env_app.base64_to_string(data['data'].get('content'))
                if data['data'].get('name'):
                    data['data']['name'] = env_app.base64_to_string(data['data'].get('name'))
                if data['data'].get('sender_name'):
                    data['data']['sender_name'] = env_app.base64_to_string(data['data'].get('sender_name'))

            if isinstance(data['data'], list):
                new_list = []
                for x in data['data']:
                    if x.get('name'):
                        x['name'] = env_app.base64_to_string(x['name'])
                    if x.get('room_name'):
                        x['room_name'] = env_app.base64_to_string(x['room_name'])
                    new_list.append(x)
                data['data'] = new_list
        except Exception as e:
            pass
        return data, msg_type

    @staticmethod
    def handle_response(keyword_data):
        """
        :param keyword_data:
        keyword        天气好
        text            当然
        text_mix       NaN
        sys_exp
        pic_path       NaN
        gif_path       NaN
        video_path     NaN
        file_path      NaN
        link           NaN
        card_id        NaN
        app_info       NaN
        type          5000
        :return:
        """
        recv_type_code = keyword_data["type"]
        response = {
            "type": keyword_data["type"],
            "data": {}
        }
        if recv_type_code == env_app.WX_SEND_TEXT:
            response["data"]["content"] = str(keyword_data["text"])
        elif recv_type_code == env_app.WX_SEND_MIX_TEXT:
            response["data"]["content"] = keyword_data["text_mix"]
        elif recv_type_code == env_app.WX_SEND_PIC:
            response["data"]["path"] = os.path.join(env_app.get_pic_path(), keyword_data["pic_path"])
        elif recv_type_code == env_app.WX_SEND_VIDEO:
            response["data"]["path"] = os.path.join(env_app.get_video_path(), keyword_data["video_path"])
        elif recv_type_code == env_app.WX_SEND_GIF:
            response["data"]["path"] = os.path.join(env_app.get_gif_path(), keyword_data["gif_path"])
        elif recv_type_code == env_app.WX_SEND_FILE:
            response["data"]["path"] = os.path.join(env_app.get_file_path(), keyword_data["file_path"])
        elif recv_type_code == env_app.WX_SEND_LINK:
            response["data"] = json.loads(keyword_data["link"])
        elif recv_type_code == env_app.WX_SEND_SYS_EXP:
            response["data"]["content"] = keyword_data["sys_exp"]
        elif recv_type_code == env_app.WX_SEND_APP:
            response["data"] = json.loads(keyword_data["app_info"])
        elif recv_type_code == env_app.WX_SEND_CARD:
            response["data"]["shared_id"] = keyword_data["card_id"]
        elif recv_type_code == env_app.WX_SEND_JOIN_ROOM:
            response["data"]["room_name"] = keyword_data["room_name"]

        return response if response != {} else False

    @staticmethod
    def re_phone(phone):
        ret = re.match(r"1[3-9]\d{9}", phone)
        if ret:
            result = True
        else:
            result = False
        return result

    @staticmethod
    def is_room(data):
        return True if data else False

    @staticmethod
    def get_title(phone):
        host = env_app.mongo_info.get('host')
        user = env_app.mongo_info.get('user')
        password = env_app.mongo_info.get('password')
        port = env_app.mongo_info.get('port')
        database = env_app.mongo_info.get('database')
        col = env_app.mongo_info.get('col')
        mongo = MongoClient(host, port, user, password, database)
        conditions = {
            '电话': phone
        }
        result = mongo.select(col, **conditions)
        return result[0]['用户层级'] if result else None
