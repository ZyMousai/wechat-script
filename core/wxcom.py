# 企业微信基础操作
# ERIC SUN 2020-9-24
from env import env_app
from ctypes import *
import json
import copy

C_ID = 0


# 回调函数
@WINFUNCTYPE(None, c_ulong)
def connect_callback(client_id):
    print(u'新的客户端连接: ')
    global C_ID
    C_ID = client_id
    print(client_id)
    print('[on_connect] client_id: {0}'.format(client_id))


@WINFUNCTYPE(None, c_ulong, c_char_p, c_ulong)
def recv_callback(client_id, data, length):
    jsonData = json.loads(data)
    if jsonData['type'] == 500:
        return
    print('[on_recv] client_id: {0}, message:{1}'.format(client_id, json.loads(data)))


@WINFUNCTYPE(None, c_ulong)
def close_callback(client_id):
    C_ID = 0
    print(u'已断开')


def c_string(data):
    print(data)
    return c_char_p(data.encode('utf-8'))


class WeCom:
    # 加载器
    WXLOADER = None

    def __init__(self):
        # 控制库地址
        loader_path = env_app.get_dll_path(env_app.wx_com_work)

        # 注入库地址
        inject_path = env_app.get_dll_path(env_app.vx_work)

        # 设置控制库路径
        self.WXLOADER = WinDLL(loader_path)
        # 设置注入库路径
        self.WXLOADER.WXCmdInitDllPath(c_string(inject_path))

        # 获取版本
        out = create_string_buffer(20)
        self.WXLOADER.WXCmdGetLocalWechatVersion(out, 20)
        print(out.value.decode('utf-8'))

        # 初始化socket连接
        self.WXLOADER.WXCmdInitSocket(connect_callback, recv_callback, close_callback)

        # 运行
        self.WXLOADER.WXCmdRun()
        # 打开企业微信
        # ret = self.WXLOADER.WXCmdOpenWechat()
        # print(ret)
        self.WXLOADER.WXCmdOpenWechat()

    # self.WXLOADER.WXCmdStop()

    # 发送协议
    def send(self, data):
        rs = self.WXLOADER.WXCmdSend(C_ID, json.dumps(data))
        return json.loads(rs)
