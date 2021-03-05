import os
import sys
import base64
from concurrent.futures import ThreadPoolExecutor

# 每个进程的线程数
THREAD_NUM = 15


class EnvApi(object):
    WX_RECV_CODE = 15000  # 接受消息
    WX_RECV_MIX_CODE = 15013  # 接受文字图片混合
    WX_LOGIN_SUCCESS = 11001  # 登录成功
    WX_SEND_TEXT = 5000  # 发送文本
    WX_SEND_MIX_TEXT = 5001  # 发送文字表情混合
    WX_SEND_SYS_EXP = 5002  # 发送系统表情
    WX_SEND_PIC = 5003  # 发送图片
    WX_SEND_VIDEO = 5004  # 发送视频
    WX_SEND_FILE = 5005  # 发送文件
    WX_SEND_GIF = 5006  # 发送GIF
    WX_SEND_LINK = 5007  # 发送链接
    WX_SEND_APP = 5008  # 发送小程序
    WX_SEND_CARD = 5009  # 发送名片
    WX_SET_PHONE = 3005  # 设置手机号
    WX_SET_TITLE = 3007  # 设置标签
    WX_RECV_LABEL = 12504
    WX_SEND_LABEL = 2504
    WX_SEND_SEARCH_FRIEND = 3000  # 发送搜索好友指令
    WX_RECV_SEARCH_FRIEND = 13000  # 接受搜索好友指令
    WX_ADD_FRIEND = 3001  # 添加搜索的好友
    WX_ERROR_OFTEN = 40001  # 操作频繁错误码
    WX_ERROR_NOT_EXIST = 43003  # 搜索用户不存在
    WX_ERROR_UNABLE = 43004  # 对方设置 无法添加好友
    WX_SEND_ROOM = 2502  # 获取群聊列表
    WX_RECV_ROOM = 22502  # 接受群聊列表
    WX_SEND_JOIN_ROOM = 4003  # 邀请好友进群

    def __init__(self):
        # todo 需要填写mongo信息
        self.mongo_info = {
            'host': '',
            'user': '',
            'password': '',
            'database': '',
            'port': '',
            'col': ''
        }
        self.vx_work = "VXWorkElf_v3.1.1.3002_release.dll"
        self.wx_com_work = "WXCommand_work.dll"
        # 线程池
        self.thread_pool = ThreadPoolExecutor(THREAD_NUM)

    @staticmethod
    def app_path():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def get_dll_path(self, dll_name):
        """
        获取dll path
        :return:
        """
        return os.path.join(self.app_path(), "tools", "dll", dll_name)

    def get_dll_dir_path(self):
        return os.path.join(self.app_path(), "tools", "dll")

    @staticmethod
    def base64_to_string(data):
        return str(base64.b64decode(data), encoding='utf-8')

    def get_phrase_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "phrase", "phrase.xlsx")

    def get_no_phrase_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "phrase", "no_phrase.xlsx")

    def get_pic_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "pic")

    def get_gif_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "gif")

    def get_file_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "file")

    def get_video_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "video")

    def get_add_account_csv(self):
        return os.path.join(self.app_path(), "tools", "im_file", "mobile_list.csv")


env_app = EnvApi()
