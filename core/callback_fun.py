"""回调函数"""
import json
import traceback
import pandas as pd
import numpy as np
from core.pubilc_fun import PublicFun
from env import env_app
from ctypes import c_char_p

TITLE_LIST = []


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
    global TITLE_LIST
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
                response = {
                    'type': env_app.WX_SET_PHONE,
                    'data': {
                        'user_id': user_id,
                        'mobile_list': [recv_content]
                    }

                }
                send(wx_obj, client_id, response)

                # 设置标签
                # query_result = PublicFun.get_title(recv_content) # todo 正式环境使用，需要链接数据库
                query_result = '一般发展客户'  # 测试用
                if query_result:
                    label_list = []
                    for label in TITLE_LIST:
                        if query_result in label['name']:
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


def label_callback_handle(wx_obj, client_id):
    response = {
        "type": env_app.WX_SEND_LABEL
    }
    send(wx_obj, client_id, response)
