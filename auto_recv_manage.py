import time
from core.wxcom import WeCom

if __name__ == '__main__':

    wx = WeCom()
    wx.open_wx()
    while True:
        time.sleep(0.5)
