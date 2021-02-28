# -*- coding:utf-8 -*-
# @Author: zy
# @Date:   2020.11.16 17:36
# @Last Modified by: zy
# @Last Modified time: 2020.11.24.16:50

import pymongo


class MongoClient(object):

    def __init__(self, host, port, username, password, database, ):
        """
        :param host: 数据库ip地址
        :param port: 数据库端口
        :param username: 用户名
        :param password: 密码
        :param database: 库名
        对mongo的增删改查通用封装
        """
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__db = None
        # 认证
        # self.__db.authenticate(username, password)
        if not self.__db:
            self.__get_conn()

    def __get_conn(self):
        # # 连接
        # self.__client = pymongo.MongoClient(
        #     'mongodb://{}:{}@{}:{}/'.format(self.__username, self.__password, self.__host, self.__port))
        # # 连接库
        # self.__db = self.__client[self.__database]

        # 连接
        self.__client = pymongo.MongoClient(self.__host, self.__port)
        # 连接库
        self.__db = self.__client[self.__database]
        # 认证
        self.__db.authenticate(self.__username, self.__password)

    def close(self):
        self.__client.close()

    def select(self, collection, **kwargs):
        """
        查询数据
        :param collection: 表名
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        return [x for x in _col.find(kwargs)]

    def add_data(self, collection, data):
        """
        新增数据,单条或者多条
        :param collection: 表明
        :param data: 新增的数据
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        if isinstance(data, dict):
            return _col.insert_one(data)
        elif isinstance(data, list):
            return _col.insert_many(data)
        else:
            raise TypeError('fun add_data >>>"data" cannot be  {}'.format(type(data)))

    def delete_data(self, collection, **kwargs):
        """
        删除数据
        :param collection: 表名
        :param kwargs: 删除条件
        :return: {u'ok': 1.0, u'n': 0}
        """
        _col = self.__db[collection]
        return _col.remove(kwargs)

    def update_data(self, collection, filters, data, is_one=True):
        """
        更新数据
        :param collection: 表名
        :param data: 更新的数据
        :param filters: 更新条件
        :param is_one: 是否更新单条
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        if is_one:
            return _col.update_one(filters, data)
        else:
            return _col.update_many(filters, data)

    def select_page(self, collection, **kwargs):
        """
        分页条件查询数据
        :param collection: 表名
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        limit_count = kwargs.pop('limit_count')
        skip_count = kwargs.pop('skip_count')
        return [x for x in _col.find(kwargs, {'_id': 0}).limit(limit_count).skip(skip_count)]

    def select_count(self, collection, **kwargs):
        """
        统计集合的数据量
        可以条件查询后统计
        :param collection: 表名
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        return self.__db[collection].count_documents(kwargs)

# # 调用案例
# if __name__ == '__main__':
#     mongo = MongoClient()
#     # 查询
#     print mongo.select(MONGO_DATA_DOC)
#     # 条件查询
#     print mongo.select(MONGO_DATA_DOC, **{'alexa': '999'})
#
#     import uuid
#
#     # 新增单条
#     print mongo.add_data(MONGO_DATA_DOC, {u'url': u'https://www.runoob.com', u'alexa': u'10', u'name': u'kkk',
#                                           'task_uuid': str(uuid.uuid1())})
#     # 新增多条
#     d = [{u'url': u'https://www.runoob.com', u'alexa': u'103', u'name': u'kkak', 'task_uuid': str(uuid.uuid1())},
#          {u'url': u'https://www.runoob.com', u'alexa': u'102', u'name': u'kksk', 'task_uuid': str(uuid.uuid1())}]
#     print mongo.add_data(MONGO_DATA_DOC, d)
#
#     # 删除
#     print mongo.delete_data(MONGO_DATA_DOC, **{'name': '2'})
#
#     # 更新单条
#     mongo.update_data(MONGO_DATA_DOC, {'url': 'https://www.runoob.com'}, {'$set': {'alexa': '999'}})
#     print mongo.select(MONGO_DATA_DOC)
#     # 更新多条
#     mongo.update_data(MONGO_DATA_DOC, {'url': 'https://www.runoob.com'}, {'$set': {'alexa': '888'}}, False)
#     print mongo.select(MONGO_DATA_DOC)

# mongo = MongoClient()
# # 查询
# print(mongo.select('task_run_info'))
# # 条件查询
# print(mongo.select('task_run_info', **{'company': 'luminati'}))


# import uuid
# import datetime
#
#
# def add_active_task(task):
#     """将需要活跃任务的数据插入到mongo"""
#
#     info = {'active_id': str(uuid.uuid1()),
#             'task_uuid': task['task_uuid'],  # task uuid
#             'task_url': task['ads_url'],  # url
#             'task_ua': task['thisUA'],  # # ua
#             'task_cookie': task['ads_cookies'],  # cookie
#             'task_user': task['ads_username'],  # 账号
#             'task_password': task['ads_password'],  # 密码
#             'task_ip': task['proxy'] if task['company'] == 'luminati' else task['proxy']['ProxyIP'],  # ip
#             'task_ip_state': task['lumipinfo']['state'] if task['company'] == 'luminati' else task['proxy']['State'],
#             # ip的洲
#             'task_ip_city': task['lumipinfo']['city'] if task['company'] == 'luminati' else task['proxy']['City'],
#             # ip的城市
#             'state': 1,  # 状态 任务的状态：1：可活跃 2.活跃成功 3.活跃失败
#             'click_id': task['versionid'],  # bi-nom的click id
#             'is_conversion': 0,  # 是否删除，0没有 1转化
#             'is_delete': 0,  # 是否删除，0没有 1删除
#             'insert_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             }
#     mongo = MongoClient()
#     mongo.add_data('active_task', info)
#
#
# test_data = {
#     'task_uuid': str(uuid.uuid1()),
#     'ads_url': 'http://baidu.com',
#     'thisUA': 'asd231sda',
#     'ads_cookies': '1asdlkhalskhjk',
#     'ads_username': 'admin',
#     'ads_password': 'admin',
#     'company': '911',
#     'proxy': {'ProxyIP': '10.10.10.10',
#               'State': 'nt',
#
#               'City': 'zhh'},
#     'versionid': str(uuid.uuid1())
#
# }
# mongo = MongoClient()
# print(mongo.select_count('active_task'))
