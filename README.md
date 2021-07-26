# 📲 我在校园打卡程序（新版）

关于登录密码错误的问题，请看[ISSUE 1](https://github.com/zimin9/WoZaiXiaoYuanPuncher/issues/1)

新版本我在校园取消了原来的token鉴权机制，改为JWSESSION与cookie进行鉴权。

本程序利用我在校园的登录接口，每次打卡时进行登录，获取最新的JWSESSION用于打卡。

因此，本程序仅需配置一次“账户与密码”即可无限期运行，不存在之前需要定期更新token的问题【未验证，有可能打脸😅】

## 🚩 快速开始

本程序目前100%基于Python编写，需要安装的第三方依赖库有`requests`。可以按照以下简要介绍进行安装部署。

### ⚙️ 相关依赖

需要安装`requests`库，可使用pip命令来安装

```python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
```

### 🔧 配置

开始使用之前，需要配置账号信息、与所使用的数据源（目前仅能从json文件读取数据，后期会加上数据库）

在 `config.ini` 中配置程序，如下

```ini
[BasicConfig]
# 数据源格式，目前仅支持json，后期会加上数据库
dataSourceType = json
# json文件的名称，可自定义。json文件切记放在根目录
jsonFileName = source.json
```

json文件中填写账号的信息，包括账号的用户名、密码、打卡相关的数据（如位置、体温等）

格式如下

```json
[
  {
  "username": "138****3210",
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
  "userId": ""
  },
  {
  "username": "111****2222",
  "password": "password",
  "temperature": "37.0",
  "latitude": "xx.36576",
  "longitude": "xxx.74577",
  "country": "中国",
  "city": "广州市",
  "district": "xx区",
  "province": "广东省",
  "township": "**街道",
  "street": "xxxxx",
  "myArea": "",
  "areacode": "",
  "userId": ""
  }
]
```

运行 `main.py` 即可进行打卡，自动化打卡的配置将在下文介绍



## ⏰ 自动化打卡

### 💻 Linux系列系统

使用cron定时执行，下面是每一小时执行一次打卡程序的例子：

```
1 * * * * python3 /home/xxxx/WoZaiXiaoYuanPuncher/main.py
```

cron的具体使用教程可以参考这篇文章：[Linux crontab 命令 ｜ 菜鸟教程](https://www.runoob.com/linux/linux-comm-crontab.html)

### 💻 Windows系统

使用系统的“定时任务设置”即可，可视化配置非常简单，参考文章：[window下设置定时任务及基本配置 ｜ cnblog](https://www.cnblogs.com/funnyzpc/p/11746439.html)

### 💻 Github Action

参考文章：[GitHub Action自动完成华工疫情打卡、网站自动签到 ｜ csdn](https://blog.csdn.net/police_1/article/details/106837694)



## 📆 相关计划

下面是本人设想的其他功能，有空将会加入到此程序中。欢迎各位同学参与本项目，一起开发，欢迎随时PR。

- [ ] 根据地址自动获取经纬度的功能（使用各大地图软件的api）
- [ ] 从数据库中读取数据（mysql、mongodb 等）
- [ ] 加入通知功能，若打卡失败，可通过钉钉机器人或诸如“喵提醒”的微信公众号发送消息
- [ ] 编写前后端界面，将添加、删除账号等操作可视化，同时可以方便查看打卡记录
- [ ] 制作Docker镜像，方便快速部署

