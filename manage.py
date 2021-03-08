import time
import multiprocessing

from core.auto_add_account import AddAccount
from core.wxcom import WeCom

ACCOUNT_NUM = 1
QUEUE_LIST = []
if __name__ == '__main__':
    while ACCOUNT_NUM > 0:
        queue = multiprocessing.Queue()
        QUEUE_LIST.append(queue)
        p = multiprocessing.Process(target=WeCom.open_wx, args=(queue,))
        ACCOUNT_NUM -= 1
        p.start()
    while True:
        # 10s 检测一下是否有文件需要导入
        time.sleep(10)
        # 以进程队列形式进行分配
        add_account = AddAccount(QUEUE_LIST)
        add_account.run()
