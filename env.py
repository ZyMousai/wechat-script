import os
import sys


class EnvApi(object):
    """环境类"""

    def __init__(self):
        self.vx_work = "VXWorkElf_v3.1.1.3002_release.dll"
        self.wx_com_work = "WXCommand_work.dll"

    def app_path(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def get_dll_path(self, dll_name):
        """
        获取dll path
        :return:
        """
        return os.path.join(self.app_path(), "tools", "dll", dll_name)

    def get_dll_dir_path(self):
        return os.path.join(self.app_path(), "tools", "dll")


env_app = EnvApi()
