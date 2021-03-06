# 企业微信基础操作
# ERIC SUN 2020-9-24
import time
import uuid

from core.callback_fun import recv_callback_handle, label_callback_handle, search_friend, room_list_callback_handle, \
    friend_list_callback_handle
from env import env_app
from ctypes import *
import json

wx_loader = None
m_queue = None
start_time = time.time()
wait_time = 20  # todo 程序启动后的等待时间
m_file_json_uuid = None


# 回调函数
@WINFUNCTYPE(None, c_ulong)
def connect_callback(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))
    with open(env_app.get_client_json_path(m_file_json_uuid), 'a+') as f:
        f.write(str(client_id) + ':')

    # env_app.thread_pool.submit(conn_callback_handle, wx_loader, client_id)


@WINFUNCTYPE(None, c_ulong, c_char_p, c_ulong)
def recv_callback(client_id, data, length):
    json_data = json.loads(data)
    type_code = json_data['type']
    no_wait_type_code = [env_app.WX_RECV_LABEL, env_app.WX_RECV_ROOM, env_app.WX_RECV_FRIEND]
    if type_code == 500:
        return
    elif type_code == 11001:
        # 获取标签列表
        env_app.thread_pool.submit(label_callback_handle, wx_loader, client_id, json_data)
        # 获取群聊列表
        env_app.thread_pool.submit(room_list_callback_handle, wx_loader, client_id)
        # 获取好友信息
        env_app.thread_pool.submit(friend_list_callback_handle, wx_loader, client_id)
        # 开启监控是否需要添加好友
        # env_app.thread_pool.submit(search_friend, wx_loader, client_id, m_queue)
        import threading
        add_friend_thread = threading.Thread(target=search_friend, args=(wx_loader, m_queue))
        add_friend_thread.start()

    # 程序等待 不到时间不启动自动接受及回复功能
    if type_code not in no_wait_type_code:
        now_time = time.time()
        if now_time - start_time <= wait_time:
            print('Still need to wait:{}s'.format(wait_time - (now_time - start_time)))
            return
    time.sleep(1)
    # 线程池 接收消息
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
        pass
        # # 控制库地址
        # loader_path = env_app.get_dll_path(env_app.wx_com_work)
        #
        # # 注入库地址
        # inject_path = env_app.get_dll_path(env_app.vx_work)
        #
        # # 设置控制库路径
        # self.WXLOADER = WinDLL(loader_path)
        # # 设置注入库路径
        # self.WXLOADER.WXCmdInitDllPath(c_string(inject_path))
        #
        # # 获取版本
        # out = create_string_buffer(20)
        # self.WXLOADER.WXCmdGetLocalWechatVersion(out, 20)
        # # print(out.value.decode('utf-8'))
        #
        # # 初始化socket连接
        # self.WXLOADER.WXCmdInitSocket(connect_callback, recv_callback, close_callback)
        #
        # global wx_loader
        # wx_loader = self.WXLOADER

    @staticmethod
    def open_wx(queue, file_json_uuid):
        # 控制库地址
        loader_path = env_app.get_dll_path(env_app.wx_com_work)

        # 注入库地址
        inject_path = env_app.get_dll_path(env_app.vx_work)

        # 设置控制库路径
        WXLOADER = WinDLL(loader_path)
        # 设置注入库路径
        WXLOADER.WXCmdInitDllPath(c_string(inject_path))

        # 获取版本
        out = create_string_buffer(20)
        WXLOADER.WXCmdGetLocalWechatVersion(out, 20)
        # print(out.value.decode('utf-8'))

        # 初始化socket连接
        WXLOADER.WXCmdInitSocket(connect_callback, recv_callback, close_callback)

        global wx_loader, m_queue, m_file_json_uuid
        m_file_json_uuid = file_json_uuid
        m_queue = queue
        wx_loader = WXLOADER
        # 运行
        WXLOADER.WXCmdRun()
        # 打开企业微信
        # ret = self.WXLOADER.WXCmdOpenWechat()
        # print(ret)
        WXLOADER.WXCmdOpenWechat()

        while True:
            time.sleep(0.5)
