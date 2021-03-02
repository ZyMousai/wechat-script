import pandas as pd
import json
from env import env_app

# phrase_set = pd.read_excel(env_app.get_phrase_path(), sheet_name="Sheet1")
# phrase_dict = phrase_set.to_dict()
# {'keyword': {0: '天气好'}, 'text': {0: '当然'}, 'type': {0: 5000}}
# print(phrase_dict)
# print(phrase_set.iloc[1]['link'])
# print(json.loads(phrase_set.iloc[1]['link']))


a = [{'label_id': '14073748999626141', 'level': 1, 'name': '非常核心', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073749137629012', 'level': 1, 'name': '有赞', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073749253630329', 'level': 2, 'name': '奖品组', 'super_id': '0', 'type': 1},
     {'label_id': '14073749253630330', 'level': 1, 'name': '优惠券用户', 'super_id': '14073749253630329', 'type': 1},
     {'label_id': '14073749253630331', 'level': 1, 'name': '实物奖品用户', 'super_id': '14073749253630329', 'type': 1},
     {'label_id': '14073749283629477', 'level': 1, 'name': '抖音', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073749360626524', 'level': 1, 'name': '闪电侠用户', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073749486624412', 'level': 1, 'name': '测试', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073749551627107', 'level': 1, 'name': '天猫-倍思影音娱乐旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073749559625904', 'level': 2, 'name': '客户属性', 'super_id': '0', 'type': 1},
     {'label_id': '14073749559625905', 'level': 1, 'name': '有车一族', 'super_id': '14073749559625904', 'type': 1},
     {'label_id': '14073749684626317', 'level': 1, 'name': '普通用户', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073749779628781', 'level': 1, 'name': '京东-倍思照明旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073749868629278', 'level': 1, 'name': '天猫-倍思家电旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073749910628648', 'level': 1, 'name': '拼多多', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073750057628443', 'level': 1, 'name': '京东-倍思家电旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073750075630026', 'level': 1, 'name': '天猫-倍思汽车用品旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073750145627423', 'level': 1, 'name': '天猫正百川旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073750298626340', 'level': 1, 'name': '常看我们历史朋友圈', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073750543627757', 'level': 2, 'name': '用户添加渠道', 'super_id': '0', 'type': 1},
     {'label_id': '14073750548628501', 'level': 1, 'name': '云集', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073750619624777', 'level': 2, 'name': '客户等级', 'super_id': '0', 'type': 1},
     {'label_id': '14073750619624778', 'level': 1, 'name': '一般', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073750619624779', 'level': 1, 'name': '重要', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073750619624780', 'level': 1, 'name': '核心', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073750663630451', 'level': 1, 'name': '唯品会', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073750797632385', 'level': 1, 'name': '社群用户', 'super_id': '14073751444629324', 'type': 1},
     {'label_id': '14073750809627331', 'level': 1, 'name': '小米有品', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073751062627063', 'level': 1, 'name': '原充电1群用户', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073751159628971', 'level': 1, 'name': '京东-倍思影音娱乐旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073751415629174', 'level': 1, 'name': '苏宁', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073751444629324', 'level': 2, 'name': '个性标签', 'super_id': '0', 'type': 1},
     {'label_id': '14073751444629325', 'level': 1, 'name': '忠实粉丝', 'super_id': '14073751444629324', 'type': 1},
     {'label_id': '14073751480628325', 'level': 1, 'name': '商务合作', 'super_id': '14073749559625904', 'type': 1},
     {'label_id': '14073751569628812', 'level': 1, 'name': '微商城', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073751778627705', 'level': 1, 'name': '天猫-倍思照明旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752053629290', 'level': 1, 'name': '京东-倍思旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752057625630', 'level': 1, 'name': '公众号', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073752137627489', 'level': 2, 'name': '用户层级', 'super_id': '0', 'type': 1},
     {'label_id': '14073752137627490', 'level': 1, 'name': '1重要价值客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627491', 'level': 1, 'name': '2重要保持客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627492', 'level': 1, 'name': '3重要发展客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627493', 'level': 1, 'name': '4重要挽留用户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627494', 'level': 1, 'name': '5一般价值客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627495', 'level': 1, 'name': '6一般发展客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627496', 'level': 1, 'name': '7一般保持客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752137627497', 'level': 1, 'name': '8一般挽留客户', 'super_id': '14073752137627489', 'type': 1},
     {'label_id': '14073752276631972', 'level': 1, 'name': '闪电侠', 'super_id': '14073751444629324', 'type': 1},
     {'label_id': '14073752375627146', 'level': 1, 'name': '拉企业群用户', 'super_id': '14073750619624777', 'type': 1},
     {'label_id': '14073752390629120', 'level': 1, 'name': '考拉', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752706631005', 'level': 1, 'name': '倍思正百川专卖店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752825630272', 'level': 1, 'name': '快手', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752847628972', 'level': 1, 'name': '京东-倍思汽车用品旗舰店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752879629701', 'level': 1, 'name': '线下门店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073752940631136', 'level': 1, 'name': '倍思启程专卖店', 'super_id': '14073750543627757', 'type': 1},
     {'label_id': '14073751138632748', 'level': 2, 'name': '个人标签', 'super_id': '0', 'type': 2}]

