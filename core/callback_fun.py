"""回调函数"""
import json
import time
import traceback
import pandas as pd
import numpy as np
import threading

from core.auto_add_account import ModifyCsv
from core.pubilc_fun import PublicFun
from env import env_app
from ctypes import c_char_p

TITLE_LIST = []
ROOM_LIST = []
FRIEND_LIST = []
LOGIN_NAME = None

lock = threading.Lock()


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def send(wx_obj, client_id, data):
    data = c_char_p(json.dumps(data, ensure_ascii=False, cls=NpEncoder).encode('utf-8'))
    wx_obj.WXCmdSend(client_id, data)


def recv_callback_handle(wx_obj, client_id, data):
    global TITLE_LIST, ROOM_LIST, FRIEND_LIST
    # 解码
    request_data, msg_type = PublicFun.handle_data(data)
    print('[on_recv] client_id: {0}, message:{1}'.format(client_id, request_data))
    core = request_data['data']
    type_code = request_data.get("type")
    # 接受消息进行判断
    if type_code == env_app.WX_RECV_CODE and msg_type:
        try:
            recv_content = core.get('content')
            if '联系人验证请求' in recv_content:
                friend_list_callback_handle(wx_obj, client_id)
                return
            is_room_msg = PublicFun.is_room(core.get('is_room_msg'))
            is_room = core.get('conversation_id')
            if 'R' in is_room:
                pass
            else:
                assert recv_content, 'The content of the received message is empty.'
                # 1.识别content是否为手机号
                phone_content = PublicFun.get_phone(recv_content)  # 获取手机号
                if phone_content:
                    if PublicFun.re_phone(phone_content) and not is_room_msg:
                        # 设置手机号
                        user_id = request_data['data']['conversation_id'].split('_')[-1]
                        mobile_list = []
                        label_list_old = []
                        for user_info in FRIEND_LIST:
                            if user_info.get('user_id') == user_id:
                                mobile_list = user_info.get('mobile_list') if user_info.get('mobile_list') else []
                                if len(mobile_list) == 5:
                                    mobile_list.sort()
                                    mobile_list.pop(0)
                                label_list_old = user_info.get('label_list') if user_info.get('label_list') else []
                                break

                        mobile_list.append(phone_content)
                        response = {
                            'type': env_app.WX_SET_PHONE,
                            'data': {
                                'user_id': user_id,
                                'mobile_list': mobile_list
                            }
                        }
                        send(wx_obj, client_id, response)

                        time.sleep(1)
                        # 设置标签
                        # query_result = PublicFun.get_title(recv_content) # todo 正式环境使用，需要链接数据库
                        # 重要保持客户 重要发展客户 重要挽留用户 一般价值客户 一般发展客户 一般保持客户
                        query_result = '一般价值客户'  # 测试用 生产环境用上面todo代码
                        if query_result:
                            label_list = []
                            for label in TITLE_LIST:
                                if query_result in label['name']:
                                    label_list.append(label['label_id'])
                            for label_name_old in label_list_old:
                                for label in TITLE_LIST:
                                    if label_name_old in label['name']:
                                        label_list.append(label['label_id'])
                            response = {
                                "type": env_app.WX_SET_TITLE,
                                "data": {
                                    "user_id": user_id,
                                    "label_id_list": label_list
                                }
                            }
                            send(wx_obj, client_id, response)
                        # 更新friend_list
                        friend_list_callback_handle(wx_obj, client_id)
                        # return

                # 2.识别否词库
                no_phrase_set = pd.read_excel(env_app.get_no_phrase_path(), sheet_name="Sheet1")
                no_keyword = np.array(no_phrase_set['keyword'])
                for no_p_s in no_keyword:
                    if no_p_s in recv_content:
                        return

                # 3.识别关键词库
                phrase_set = pd.read_excel(env_app.get_phrase_path(), sheet_name="Sheet1")
                # phrase_dict 示例 {'keyword': {0: '天气好'}, 'text': {0: '当然'}, 'type': {0: 5000}}
                phrase_dict = phrase_set.to_dict()
                for k, v in phrase_dict['keyword'].items():
                    # 4.回复
                    if v in recv_content:
                        keyword_data = phrase_set.iloc[k]
                        response = PublicFun.handle_response(keyword_data)
                        # 邀请成员进入群
                        if response['type'] == env_app.WX_SEND_JOIN_ROOM:
                            room_name = response['data'].pop('room_name')
                            for room_info in ROOM_LIST:
                                if room_info['room_name'] == room_name:
                                    room_id = room_info['room_chat_id'].split(":")[-1]
                                    response['data'] = {
                                        'room_id': room_id,
                                        'member_list': [request_data['data']['conversation_id'].split("_")[-1]]
                                    }
                                    print(response)
                                    send(wx_obj, client_id, response)
                                    break
                                else:
                                    pass
                            continue
                        # 关键词设置标签
                        if response['type'] == env_app.WX_SET_TITLE:
                            query_result = response['data']['content']
                            user_id = request_data['data']['conversation_id'].split('_')[-1]
                            label_list_old = []
                            for user_info in FRIEND_LIST:
                                if user_info.get('user_id') == user_id:
                                    label_list_old = user_info.get('label_list') if user_info.get('label_list') else []
                                    break
                            if query_result:
                                label_list = []
                                for label in TITLE_LIST:
                                    if query_result in label['name']:
                                        label_list.append(label['label_id'])
                                for label_name_old in label_list_old:
                                    for label in TITLE_LIST:
                                        if label_name_old in label['name']:
                                            label_list.append(label['label_id'])
                                response = {
                                    "type": env_app.WX_SET_TITLE,
                                    "data": {
                                        "user_id": user_id,
                                        "label_id_list": label_list
                                    }
                                }
                            print(response)
                            send(wx_obj, client_id, response)
                            # 更新friend_list
                            friend_list_callback_handle(wx_obj, client_id)
                            # return
                        # 正常回复
                        if response:
                            if is_room_msg:
                                response['data']['receiver'] = r'R:{}'.format(request_data['data']['receiver'])
                            else:
                                response['data']['conversation_id'] = request_data['data']['conversation_id']
                            print(response)
                            send(wx_obj, client_id, response)

        except Exception as e:
            print(traceback.format_exc())

    if type_code == env_app.WX_RECV_LABEL:
        TITLE_LIST = core

    if type_code == env_app.WX_RECV_SEARCH_FRIEND:
        try:
            if env_app.M_LOCK.acquire():
                # 接收到13000 更新好友缓存列表
                friend_list_callback_handle(wx_obj, client_id)
                error = request_data.get("error")
                if error == env_app.WX_ERROR_OFTEN or error == env_app.WX_ERROR_NOT_EXIST or \
                        error == env_app.WX_ERROR_UNABLE or error == env_app.WX_ERROR_UNABLE_2 or \
                        error == env_app.WX_ERROR_UNKNOWN:
                    ModifyCsv.modify_csv(core["mobile"], client_id, error)
                else:
                    # 设置手机号
                    time.sleep(1)
                    response = {
                        'type': env_app.WX_SET_PHONE,
                        'data': {
                            'user_id': core["user_id"],
                            'mobile_list': [core["mobile"]]
                        }
                    }
                    send(wx_obj, client_id, response)

                    response = {
                        "type": env_app.WX_ADD_FRIEND,
                        "data": {
                            "user_id": core["user_id"],
                            "verifytext": "你好",
                            "verifycode": core["verifycode"],
                            "rsakey": core.get('rskey', '')
                        }
                    }
                    send(wx_obj, client_id, response)

                    ModifyCsv.modify_csv(core["mobile"], client_id)
        finally:
            env_app.M_LOCK.release()
    if type_code == env_app.WX_RECV_ROOM:
        ROOM_LIST = core
    if type_code == env_app.WX_RECV_FRIEND:
        try:
            if lock.acquire():
                FRIEND_LIST = core
        finally:
            lock.release()


def label_callback_handle(wx_obj, client_id, data):
    # 记录登录的名字
    global LOGIN_NAME
    request_data, msg_type = PublicFun.handle_data(data)
    core = request_data['data']
    LOGIN_NAME = core['name']
    print('login client_id:{},login name:{}'.format(client_id, LOGIN_NAME))
    with open(env_app.get_client_name_path(), 'a+') as f:
        f.write(str(client_id) + ':' + LOGIN_NAME)
        f.write('\n')
    # 获取标签
    response = {
        "type": env_app.WX_SEND_LABEL
    }
    send(wx_obj, client_id, response)


def room_list_callback_handle(wx_obj, client_id):
    # 获取群聊列表
    response = {
        "type": env_app.WX_SEND_ROOM
    }
    send(wx_obj, client_id, response)


def friend_list_callback_handle(wx_obj, client_id):
    # 获取好友列表
    response = {
        "type": env_app.WX_SEND_FRIEND
    }
    send(wx_obj, client_id, response)


def search_friend(wx_obj, queue):
    import time
    while True:
        if not queue.empty():
            get_obj = queue.get()
            response = {
                "type": env_app.WX_SEND_SEARCH_FRIEND,
                "data": {
                    "mobile": get_obj["phone"]
                }
            }
            client_id = int(get_obj.get('client_id'))
            send(wx_obj, client_id, response)
            print('*' * 30)
            print('login client_id:{},add phone:{}'.format(client_id, get_obj["phone"]))
            print('*' * 30)
            time.sleep(10)
        else:
            time.sleep(30)
