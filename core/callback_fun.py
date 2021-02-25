"""回调函数"""
import json
import pandas as pd
import numpy as np
from core.pubilc_fun import handle_data
from env import env_app

WX_RECV_CODE = 15001  # 接受消息
WX_RECV_MIX_CODE = 15013  # 接受文字图片混合
WX_LOGIN_SUCCESS = 11001  # 登录成功

USER_ID = None
def send(wx_obj, client_id, data):
    rs = wx_obj.WXCmdSend(client_id, json.dumps(data))
    return json.loads(rs)


def recv_callback_handle(wx_obj, client_id, data):
    request_data = handle_data(data)
    print('[on_recv] client_id: {0}, message:{1}'.format(client_id, request_data))

    type_code = request_data.get("type")

    if type_code == WX_LOGIN_SUCCESS:
        global USER_ID
        USER_ID = request_data['data']['user_id']
    if type_code == WX_RECV_CODE or type_code == WX_RECV_MIX_CODE:
        result = pd.read_excel(env_app.get_phrase_path(), sheet_name="Sheet1")
        keyword = np.array(result['keyword'])
        print(keyword)
        receiver_id = request_data['data']['receiver']
        response = {
            "type": 5000,
            "data": {
                "conversation_id": "S:{}_{}".format(USER_ID, receiver_id),
                "content": "你好",
                "use_utf8_base64_encode": 1
            }
        }
        print(response)
        sss = send(wx_obj, client_id, response)
        print(sss)
