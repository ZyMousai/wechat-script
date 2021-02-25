import time

import pandas as pd

from core.wxcom import WeCom
from env import env_app

if __name__ == '__main__':

    wx = WeCom()
    wx.open_wx()
    while True:
        time.sleep(0.5)