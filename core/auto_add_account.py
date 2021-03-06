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
        error_msg = None
        # 读取
        df_result = pd.read_csv(env_app.get_add_account_csv())
        # 获取phone的index
        phone = int(phone)
        phone_index = df_result[df_result["phone"] == phone].index
        # 获取who_add 是哪一列
        who_add_index = list(df_result.columns).index('who_add')
        # 获取is_success 是哪一列
        is_success_index = list(df_result.columns).index('is_success')
        if error == env_app.WX_ERROR_UNABLE:
            error_msg = "对方设置 无法添加好友"
        elif error == env_app.WX_ERROR_NOT_EXIST:
            error_msg = "搜索用户不存在"
        elif error_msg == env_app.WX_ERROR_OFTEN:
            error_msg = "操作频繁"
        if error and error_msg:
            # 获取error 是哪一列
            error_index = list(df_result.columns).index('error')
            # 修改error 信息
            df_result.iloc[phone_index, error_index] = error_msg
            # 修改is_success 信息
            df_result.iloc[phone_index, is_success_index] = 2
        else:
            # 修改is_success 信息
            df_result.iloc[phone_index, is_success_index] = 1
        # 修改who_add 信息
        df_result.iloc[phone_index, who_add_index] = who_add
        # 保存到csv
        df_result.to_csv(env_app.get_add_account_csv())
