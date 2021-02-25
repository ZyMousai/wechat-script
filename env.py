import os
import sys
import base64
from concurrent.futures import ThreadPoolExecutor

THREAD_NUM = 30


class EnvApi(object):

    def __init__(self):
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
        """
        解码
        :param data:
        :return:
        """
        return str(base64.b64decode(data), encoding='utf-8')

    def get_phrase_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "phrase", "phrase.xlsx")

    def get_no_phrase_path(self):
        return os.path.join(self.app_path(), "tools", "auto_recv", "phrase", "no_phrase.xlsx")

env_app = EnvApi()
