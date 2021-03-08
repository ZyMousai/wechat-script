# wechat-script
##开发环境
1. python3.7.3 32bit
2. 依赖包 requirements.txt
3. 安装依赖 pip install -r requirements.txt

### 目录说明
#### core 核心代码
1. callback_fun.py 主要功能回调函数
2. mongo_client mongo封装
3. pubilc_fun 公共方法
4. wxcom.py 调用dll
5. auto_add_account.py 自动添加好友相关
#### tools 工具包
1. auto_recv 自动回复使用到的工具
2. auto_rect/phrase/base_phrase.csv 为模板文件，填入自己需要的修改为phrase.csv程序方可触发
2. dll
3. im_file 导入自动添加好友使用
4. im_file/mobile_list.csv 为自动导入好友文件，使用需要填入phone和is_success字段。
#### env 全局
#### manage.py 程序入口

### 版本历史
| 版本号 | 时间 | 说明 |
|----|----|----|
|1.0|2021-3-5|交付测试1.0|
|1.1|2021-3-8|修复群邀请、改善添加好友、增加多种错误码|