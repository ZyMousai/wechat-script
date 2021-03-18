import time
import multiprocessing
import uuid

from core.auto_add_account import AddAccount
from core.wxcom import WeCom

ACCOUNT_NUM = 2
QUEUE_LIST = []
file_json_uuid = str(uuid.uuid1()) + '.txt'
if __name__ == '__main__':
    queue = multiprocessing.Queue()
    QUEUE_LIST.append(queue)
    while ACCOUNT_NUM > 0:
        p = multiprocessing.Process(target=WeCom.open_wx, args=(queue, file_json_uuid,))
        ACCOUNT_NUM -= 1
        p.start()
    while True:
        # 等待30s 准备开始检测是否有文件需要导入
        time.sleep(60)
        # 以进程队列形式进行分配
        add_account = AddAccount(QUEUE_LIST, file_json_uuid)
        add_account.run()
        # 检测完毕 下一轮300S后开始
        time.sleep(300)
