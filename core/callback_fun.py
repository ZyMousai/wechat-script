"""回调函数"""
import json
import traceback
import pandas as pd
import numpy as np

from core.auto_add_account import ModifyCsv
from core.pubilc_fun import PublicFun
from env import env_app
from ctypes import c_char_p

TITLE_LIST = []
ROOM_LIST = []
FRIEND_LIST = []
LOGIN_NAME = None


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
            is_room_msg = PublicFun.is_room(core.get('is_room_msg'))
            assert recv_content, 'The content of the received message is empty.'
            # 1.识别content是否为手机号
            if PublicFun.re_phone(recv_content) and not is_room_msg:
                # 设置手机号
                user_id = request_data['data']['conversation_id'].split('_')[-1]
                mobile_list = []
                label_list_old = []
                for user_info in FRIEND_LIST:
                    if user_info.get('user_id') == user_id:
                        mobile_list = user_info.get('mobile_list') if user_info.get('mobile_list') else []
                        label_list_old = user_info.get('label_list') if user_info.get('label_list') else []
                        break

                mobile_list.append(recv_content)
                response = {
                    'type': env_app.WX_SET_PHONE,
                    'data': {
                        'user_id': user_id,
                        'mobile_list': mobile_list
                    }
                }
                send(wx_obj, client_id, response)

                # 设置标签
                # query_result = PublicFun.get_title(recv_content) # todo 正式环境使用，需要链接数据库
                query_result = '一般发展客户'  # 测试用 生产环境用上面todo代码
                if query_result:
                    label_list = []
                    for label_name_old in label_list_old:
                        for label in TITLE_LIST:
                            if query_result in label['name']:
                                label_list.append(label['label_id'])
                            elif label_name_old in label['name']:
                                label_list.append(label['label_id'])
                    response = {
                        "type": env_app.WX_SET_TITLE,
                        "data": {
                            "user_id": user_id,
                            "label_id_list": label_list
                        }
                    }
                    send(wx_obj, client_id, response)
                return

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
                        return
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
        error = request_data.get("error")
        if error == env_app.WX_ERROR_OFTEN or error == env_app.WX_ERROR_NOT_EXIST or \
                error == env_app.WX_ERROR_UNABLE or error == env_app.WX_ERROR_UNABLE_2 or \
                error == env_app.WX_ERROR_UNKNOWN:
            ModifyCsv.modify_csv(core["mobile"], LOGIN_NAME, error)
        else:
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
            ModifyCsv.modify_csv(core["mobile"], LOGIN_NAME)

    if type_code == env_app.WX_RECV_ROOM:
        ROOM_LIST = core
    if type_code == env_app.WX_RECV_FRIEND:
        FRIEND_LIST = core


def label_callback_handle(wx_obj, client_id, data):
    # 记录登录的名字
    global LOGIN_NAME
    request_data, msg_type = PublicFun.handle_data(data)
    core = request_data['data']
    LOGIN_NAME = core['name']
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
    # 获取群聊列表
    response = {
        "type": env_app.WX_SEND_FRIEND
    }
    send(wx_obj, client_id, response)


def search_friend(wx_obj, client_id, queue):
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
            send(wx_obj, client_id, response)
            time.sleep(15)
        else:
            time.sleep(30)
