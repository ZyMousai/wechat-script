"""公共方法"""
from env import env_app


def handle_data(data):
    """
    处理数据
    :param data:
    :return:
    """
    if data['data'].get('content'):
        data['data']['content'] = env_app.base64_to_string(data['data'].get('content'))
    if data['data'].get('name'):
        data['data']['name'] = env_app.base64_to_string(data['data'].get('name'))
    if data['data'].get('sender_name'):
        data['data']['sender_name'] = env_app.base64_to_string(data['data'].get('sender_name'))
    return data

