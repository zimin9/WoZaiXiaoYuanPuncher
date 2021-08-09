# WoZaiXiaoYuanPuncher-cloudFunction

我在校园自动打卡程序：[WoZaiXiaoYuanPuncher](https://github.com/zimin9/WoZaiXiaoYuanPuncher) 的云函数版本

### 版本说明

核心代码来自于 [WoZaiXiaoYuanPuncher](https://github.com/zimin9/WoZaiXiaoYuanPuncher)。这个版本在原有代码的基础上做了一点修改，可以实现**云函数自动打卡 + 消息提醒**。只需要在云端部署函数，本地不需要做任何处理，打卡结果会自动发送到微信上。

### 更新情况

2021-8-9

* 根据所在城市和学校名自动获取所有地址信息并进行存储，无需再进行抓包和手动配置
* 减少大量配置项

2021-8-8

* 云函数不支持通过读写文件的方式持久化存储数据，且云数据库收费，因此接入 leanCloud 存储数据

2021-8-4 

* 消息提醒服务从喵提醒改为 pushPlus，不需要再手动激活 48 小时
* 缓存 jwsession 到本地，避免频繁登录可能导致的账户出错问题v
* 优化代码结构

### 使用方法

#### 0. 克隆项目到本地

```ba
git clone git@github.com:Chorer/WoZaiXiaoYuanPuncher-cloudFunction.git
```

#### 1. 获取 pushPlus 的 token

微信搜索公众号“pushplus 推送加”，关注后即可生成属于自己的 token，后面需要用到

#### 2. 获取 leanCloud 的应用凭证

1）[注册 leanCloud 账号](https://console.leancloud.cn/apps) 

2）到控制台新建应用，应用名字随意，应用版本选择 **开发版**

3）进入应用，点击左侧的“数据存储 ➡ 结构化数据”，新建 Class：名称为“Info”，Class 访问权限为“所有用户”，下面的 ACL 权限选择“限制写入”

4）进入刚才创建的 Class，添加新列，值为“jwsession”；如果你知道如何抓包获取自己的 jwsession，则添加新行并填入 jwsession 值，否则不用管它。

5）点击左侧的“设置 ➡ 应用凭证”，记住 appId 和 masterKey（**请务必自己保管好，不要泄露**） 的值，待会需要用到


#### 3. 创建云函数

1）注册腾讯云账号并登录，进行实名认证

2）到 https://console.cloud.tencent.com/scf/list?rid=1&ns=default ，选择 “新建云函数” ➔ “自定义创建”，提交方法选择“本地上传文件夹”，选中 `WoZaiXiaoYuanPuncher-cloudFunction/src` 文件夹上传，点击“完成”即可创建云函数

#### 4. 修改配置文件

到刚才新创建的云函数中，打开 `config.json` 配置文件进行修改。

1）“我在校园”账号配置项说明：

* `username`：“我在校园”的账号，一般是你的手机号码
* `password`：“我在校园”的密码，忘记了打开小程序重新设置就行
* `temperature`：默认上报的体温为 36°C，如果你想随机上报体温，请以“36~38”的形式填写
* `city`：你学校所在的城市
* `school`：你学校的名字

2）“pushPlus” 账号配置项说明：

* `isEnable`：默认 `false`，表示不开启消息提醒功能，若要开启请修改为 `true`
* `notifyToken`：之前你从 pushPlus 公众号那里获取的 token

3）“leanCloud” 账号配置项说明：

* `appId`：之前在 leanCloud 获取的 appId
* `masterKey`：之前在 leanCloud 获取的 masterKey

#### 5. 安装 leanCloud 库

到刚才新创建的云函数中，`ctrl + shift + ~` 新建终端，cd 进入 `index.py` 所在的文件夹中，通过如下命令安装 leanCloud 库：

```cmd
pip3 install leancloud -t .
```

可能会报错，主要是因为相关库版本不匹配的问题，不影响正常使用。看到 `successfully installed` 就说明安装成功了。

#### 6. 部署和测试

修改完成后点击部署并测试，如果微信有收到 pushPlus 公众号发来的信息，说明设置 ok。效果如下图所示：

1）客服消息：
![](https://myblog-1258623898.cos.ap-chengdu.myqcloud.com/pr/2.jpg)

2）模板消息：
![](https://myblog-1258623898.cos.ap-chengdu.myqcloud.com/pr/1.jpg)

默认发送的是客服消息，如果发送的消息数量超过微信限制，则会降级为模板消息。通过给公众号发送“激活消息”四个字，可以重新激活客服消息功能。但无论是哪一种，你都是可以收到消息的，所以就算不激活也没事。

#### 7. 实现自动打卡

点击控制台左侧的“触发管理”，新建一个云函数触发器。设置如下：

![](https://myblog-1258623898.cos.ap-chengdu.myqcloud.com/pr/image-20210802123156661.png)

触发时间使用的是 Cron 表达式，这里的意思是每天 7 点、13 点、19 点各触发（打卡）一次，可以自己修改，按照自己学校规定的打卡时间段来设置。

最后提交就可以了，以后到点了就会自动打卡并把打卡结果发到你的微信上。

### Q & A

**1）云函数服务收费吗？**

免费。免费调用额度是 100 万次/月，正常用户最多调用 900 次/月，因此绝对够用

**2）都用云函数了，为什么不直接链接云数据库？**

云数据库没有免费额度，没必要为了存储一个 jwsession 花钱

**3）leanCloud 服务收费吗？**

免费。开发版的免费额度是 1GB/天，因此绝对够用

**4）收到消息说“登录失败，请检查账号信息”，应该怎么办？**

待优化功能。很可能是因为频繁登录导致的，这时候就别依赖云函数模拟登录获取 jwsession 了，请自己手动抓包获取 jwsession，填入 leanCloud 的 Class 中 

**5）不能自动定位吗？**
初始的想法是通过“请求地址的 ip ➡ 经纬度 ➡ 具体地址”这样的路径获取一个结构化的地址，用户无需进行任何配置，但是 PC 上定位经常不准（比如说我用 PC 端小程序打卡，定位的也是另一个市区）。所以最终还是通过“城市名+学校名 ➡ 经纬度 ➡ 具体地址”来拿到地址，无论如何，配置项已经非常少了。

**6）地址是否准确？**
脚本使用的是和小程序一样的高德地图 API，准确性基本没问题                      

**7）leanCloud 库可以选择其它安装路径吗？**

不建议。你需要通过 `sys.path` 修改导包路径，很麻烦，而且会遇到其它依赖导入路径出错的问题。所以最简单的方法就是直接安装在 `index.py` 的所在路径下。

### 鸣谢

* [@zimin9：WoZaiXiaoYuanPuncher](https://github.com/zimin9/WoZaiXiaoYuanPuncher)

### 声明

- 本项目仅供编程学习/个人使用，请遵守Apache-2.0 License开源项目授权协议
- 请在国家法律法规和校方相关原则下使用
- 开发者不对任何下载者和使用者的任何行为负责
- 无任何后门，也不获取、存储任何信息
- 请务必不要泄露你的 masterKey 或 jwsession





