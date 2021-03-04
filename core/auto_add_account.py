from env import env_app
import pandas as pd


class AddAccount(object):
    def __init__(self, queue_list):
        self.queue_list = queue_list
        self.file_path = env_app.get_add_account_csv()
        self.add_result = None
        self.original_result = None
        self.put_list = []

    def __read_file(self):
        # 状态码 is_success 0未添加 1添加成功 2添加错误
        df_result = pd.read_csv(self.file_path)
        self.original_result = df_result
        self.add_result = df_result[df_result['is_success'] == 0]

    def __create_put_list(self):
        for index, row in self.add_result.iterrows():
            put_dict = {
                "index": index,
                "phone": str(int(row["phone"])),
                "is_success": int(row["is_success"]),
                "who_add": None,
                "error": None
            }
            self.put_list.append(put_dict)

    def __dispatch(self):
        """调度及分配到队列"""
        q_index = -1
        for put_obj in self.put_list:
            for q in self.queue_list:
                now_q_index = self.queue_list.index(q)
                last_q_index = self.queue_list.index(self.queue_list[-1])
                if q_index != now_q_index and q_index < now_q_index:
                    q.put(put_obj)
                    if now_q_index == last_q_index:
                        q_index = -1
                    else:
                        q_index = now_q_index
                    break

    def run(self):
        # 读取文件
        self.__read_file()
        # 读取出来df不为空则生成 添加账号数据对象 放进队列
        if not self.add_result.empty:
            self.__create_put_list()
            self.__dispatch()


class ModifyCsv(object):
    @staticmethod
    def modify_csv(phone, who_add, error=None):
        pass
