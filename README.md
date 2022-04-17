### 💡 2022.04.17 我在校园更新，本脚本已失效。

# 📲 新版我在校园打卡程序

**关于登录密码错误的问题，请看[ISSUE 1](https://github.com/zimin9/WoZaiXiaoYuanPuncher/issues/1)、[ISSUE 13](https://github.com/zimin9/WoZaiXiaoYuanPuncher/issues/13)**

新版本我在校园取消了原来的token鉴权机制，改为JWSESSION与cookie进行鉴权。

本程序通过登录接口获取、维护有效jwsession进行打卡，理论上仅需配置一次“账户与密码”即可无限期运行。

#### 本次更新：

1. 增加轻量级数据库SQLite，在首次登陆后，记录账号的jwsession，避免频繁登陆导致账号异常/冻结（与登录有关的问题可以看[ISSUE 1](https://github.com/zimin9/WoZaiXiaoYuanPuncher/issues/1)）。当jwsession失效时，程序才会再次发起登陆、更新jwsession。
2. 增加PushPlus、钉钉机器人推送提醒功能


## 🚩 快速开始

本程序目前100%基于Python编写，需要安装的第三方依赖库有`requests`。可以按照以下简要介绍进行安装部署。

### ⚙️ 相关依赖

需要安装`requests`库，可使用pip命令来安装

```python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
```

### 🔧 配置

开始使用之前，需要进行相应配置

Ⅰ.  在 `main.py` 中配置相关路径（请填写绝对路径），如下

```python
# 填写SQLite的绝对路径，使用cron定时执行脚本时不要用相对路径！（找到项目根目录下的database.sqlite文件，复制其绝对路径）
SQLITE_DIR = "Z:\\Users\\WoZaiXiaoYuanPuncher\\database.sqlite"

# 填写json文件的绝对路径
JSON_FILE = "Z:\\Users\\WoZaiXiaoYuanPuncher\\source.json"
```

Ⅱ.  在json文件中填写账号的信息，包括账号的用户名(username)、密码(password)、打卡相关的数据（如位置、体温等）

可以配置多个账户进行打卡，字段名即字段含义，格式如下

​	✏ 其中 `notification_type` 可指定使用的推送平台，目前支持PushPlus与钉钉机器人两种通知方式。若使	用PushPlus请填写“PushPlus”，若使用钉钉机器人请填写“DingDing”，若不使用推送提醒功能填“None”。 

​	✏ `notify_token` 填写对应推送平台的token（钉钉机器人则填写secret）

​	✏ `dingding_access_token` 填写钉钉机器人的access_token

```json
[
  {
  "username": "135****1234",
  "password": "password",
  "temperature": "37.0",
  "latitude": "23.36576",
  "longitude": "113.74577",
  "country": "中国",
  "city": "广州市",
  "district": "海珠区",
  "province": "广东省",
  "township": "**街道",
  "street": "仑头路xx号",
  "myArea": "",
  "areacode": "",
  "userId": "",
  "notification_type": "PushPlus",
  "notify_token": "",
  "dingding_access_token": "" 
  },
  {
  "username": "123****0000",
  "password": "password",
  "temperature": "37.0",
  "latitude": "23.36576",
  "longitude": "113.74577",
  "country": "中国",
  "city": "广州市",
  "district": "海珠区",
  "province": "广东省",
  "township": "**街道",
  "street": "仑头路xx号",
  "myArea": "",
  "areacode": "",
  "userId": "",
  "notification_type": "DingDing",
  "notify_token": "",
  "dingding_access_token": ""
  }
]
```

运行 `main.py` 即可进行打卡，自动化打卡的配置将在下文介绍

Ⅲ. 若数据库表格有误，可复制下列SQL建表：

```sql
create table jwsession
(
    username    text not null
        constraint jwsession_pk
            primary key,
    jwsession   text,
    update_time text,
    is_valid    integer
);
```



## ⏰ 自动化打卡

### 💻 Linux系列系统

使用cron定时执行，下面是每小时（的第一分钟时）执行一次打卡程序的例子：

```
1 * * * * python3 /home/xxxx/WoZaiXiaoYuanPuncher/main.py
```

cron的具体使用教程可以参考这篇文章：[Linux crontab 命令 ｜ 菜鸟教程](https://www.runoob.com/linux/linux-comm-crontab.html)

### 💻 Windows系统

使用系统的“定时任务设置”即可，可视化配置非常简单，参考文章：[window下设置定时任务及基本配置 ｜ cnblog](https://www.cnblogs.com/funnyzpc/p/11746439.html)

### 💻 Github Action
[jimlee2002/WoZaiXiaoYuanPuncher-Actions](https://github.com/jimlee2002/WoZaiXiaoYuanPuncher-Actions)

### 💻 云函数打卡
[Chorer/WoZaiXiaoYuanPuncher-cloudFunction](https://github.com/Chorer/WoZaiXiaoYuanPuncher-cloudFunction)

### 💻 Docker版本
[ccqstark/WoZaiXiaoYuanPuncher-Docker](https://github.com/ccqstark/WoZaiXiaoYuanPuncher-Docker)

## 🚀 贡献者(Contributors)

✨ 感谢 [Chorer](https://github.com/Chorer) 贡献 云函数与消息提醒代码

✨ 感谢 [jimlee2002](https://github.com/jimlee2002) 贡献 Github Action版代码与健康打卡功能

✨ 感谢 [ccqstark](https://github.com/ccqstark) 贡献 Docker版代码

## 📆 相关计划

下面是本人设想的其他功能，有空将会加入到此程序中。欢迎各位同学参与本项目，一起开发，欢迎随时PR。

- [ ] 根据地址自动获取经纬度的功能（使用各大地图软件的api）
- [x] 从数据库中读取数据
- [x] 加入通知功能，若打卡失败，可通过钉钉机器人或诸如“喵提醒”的微信公众号发送消息
- [x] 制作Docker镜像，方便快速部署

## 📢 声明
1. 本项目仅供编程学习/个人使用，请遵守Apache-2.0 License开源项目授权协议。
2. 请在国家法律法规和校方相关原则下使用。
3. 开发者不对任何下载者和使用者的任何行为负责。
4. 本程序无任何后门，所有数据仅存留于使用者机器上。 
5. 请不要轻易将自己的账号信息告诉他人。
