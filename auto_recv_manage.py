import time
import multiprocessing
from core.wxcom import WeCom

ACCOUNT_NUM = 1
if __name__ == '__main__':

    while ACCOUNT_NUM > 0:
        # p = threading.Thread(target=wx.open_wx)
        p = multiprocessing.Process(target=WeCom.open_wx)
        ACCOUNT_NUM -= 1
        p.start()
    while True:
        time.sleep(0.5)
