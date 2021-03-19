# wechat-script
## 开发环境
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
3. dll
4. im_file 导入自动添加好友使用
5. im_file/mobile_list.csv 为自动导入好友文件，使用需要填入phone和is_success字段。
6. client_json 为存储client_id的配置文件，可删除
7. client_name.txt 为client_id和name的映射
#### env 全局
#### manage.py 程序入口

### 版本历史
| 版本号 | 时间 | 说明 |
|----|----|----|
|1.0|2021-3-5|交付测试1.0|
|1.1|2021-3-8|修复群邀请、改善添加好友、增加多种错误码|
|1.2|2021-3-9|修改手机号标签为累加,修复名片添加，改善添加好友|
|1.3|2021-3-10|添加只要有11位连续数字就进行匹配手机号功能|
|1.4|2021-3-13|添加开启程序3分钟后处理消息，添加新增好友刷新缓存|
|1.5|2021-3-17|修改手机号及群邀请后继续触发回复，添加好友增加线程锁，添加手机号如果满了进行正序排序|
|1.6|2021-3-17|修复添加好友异常|
|1.7|2021-3-18|修改添加好友位单队列记录client_id的方式|
|1.8|2021-3-19|增加添加好友前给用户设置手机号|