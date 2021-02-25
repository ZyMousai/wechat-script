# 企业微信基础操作
# ERIC SUN 2020-9-24
from core.callback_fun import recv_callback_handle
from env import env_app
from ctypes import *
import json

wx_loader = None


# 回调函数
@WINFUNCTYPE(None, c_ulong)
def connect_callback(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))


@WINFUNCTYPE(None, c_ulong, c_char_p, c_ulong)
def recv_callback(client_id, data, length):
    json_data = json.loads(data)
    if json_data['type'] == 500:
        return
    env_app.thread_pool.submit(recv_callback_handle, wx_loader, client_id, json_data)


@WINFUNCTYPE(None, c_ulong)
def close_callback(client_id):
    print('[on_close] client_id: {0}'.format(client_id))


def c_string(data):
    # print(data)
    return c_char_p(data.encode('utf-8'))


class WeCom:
    # 加载器
    # WXLOADER = None

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
        # print(out.value.decode('utf-8'))

        # 初始化socket连接
        self.WXLOADER.WXCmdInitSocket(connect_callback, recv_callback, close_callback)

        global wx_loader
        wx_loader = self.WXLOADER

    # self.WXLOADER.WXCmdStop()

    def open_wx(self):
        # 运行
        self.WXLOADER.WXCmdRun()
        # 打开企业微信
        # ret = self.WXLOADER.WXCmdOpenWechat()
        # print(ret)
        self.WXLOADER.WXCmdOpenWechat()
