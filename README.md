
# Grasscutter-CDKeySystem - Grasscutter 外置CDKey

![主界面](image/ScreenShot1.JPG)

Grasscutter-CDKeySystem 是一个 [Grasscutter](https://github.com/Grasscutters/Grasscutter) 外置系统, 你可以用它来轻松的兑换和分发游戏的CDKey

* 已适配YSGM（MUIP）官方服务端

推荐使用 Grasscutter 命令生成工具:
[GrasscutterCommandGenerator](https://github.com/jie65535/GrasscutterCommandGenerator)

## 💡Feature

- [x] **通过opencommand连接Grasscutter.**
- [x] **通过YSGM（MUIP）连接官方服务端.**
- [x] **CDKey兑换**  - 玩家可以兑换已经生成的CDKey.
- [x] **CDKey生成**  - 管理者可以生成CDKey的内容，支持批量生成。
- [X] **开启地图和深渊**  - 玩家可以一键开启地图和深渊(仅限Grasscutter).
- [X] **设置世界等级**  - 玩家可以任意设置世界等级(仅限Grasscutter).
- [x] **远程执行**  - 可以远程执行命令.
- [x] **每日签到**  - 签到系统（默认是Grasscutter的命令，每天1000摩拉）.
- [x] **自定义背景图** - 可以自定义页面的背景图链接（比如随机图）
- [ ] **幸运抽奖**  - 抽奖系统.
- [ ] **更多**  - Comming soon...

## 🍗Setup
### 安装
注意：

一旦确定好使用的连接方式就不要更改，否则可能会由于命令语法不兼容导致执行出错！
以下两种连接方式可以任选其一：
#### 一、连接Grasscutter：
 >本项目基于 [opencommand-plugin](https://github.com/jie65535/gc-opencommand-plugin) 插件
 
1. [下载opencommand插件](https://github.com/jie65535/gc-opencommand-plugin/releases)
2. 把插件放进你的Grasscutter服务器的 `plugins` 文件夹。
3. 启动服务器，插件会自动在你的服务器插件文件夹下生成 `opencommand-plugin` 文件夹。
4. 打开 `opencommand-plugin` 文件夹，打开并编辑 `config.json`。
5. 设置 `consoleToken` 的值为你的连接秘钥，建议使用至少32字符的长随机字符串。
6. 安装Python3和依赖包：
```shell
pip install django==3.2 requests
```
7. 下载本仓库到服务器，打开并编辑`app`文件夹里的`CONSTANTS.py`文件。
8. 设置服务器地址、opencommand的Token和自定义密码，保存
>务必保证YSGM（MUIP）的enable状态为False
```python
# 设置服务器open-command的token
Server_token = 'token_value'

# 设置服务器地址，不带后边的/
Server_addr = 'https://127.0.0.1'

# 设置MeaMail插件的邮件模板文件夹（暂不需要）
MeaMail_addr = r'plugins\MeaMailPlus\template'

# 设置登录认证的密码
auth_pwd = 'jixiaob'
```
9. 在项目目录运行
```shell
python manage.py runserver 0.0.0.0:8000
```
即可在8000端口访问到页面。

#### 二、连接YSGM（MUIP）

1. 在游戏服务器部署好YSGM（MUIP）
2. 安装Python3和依赖包：
```shell
pip install django==3.2 requests
```
3. 下载本仓库到服务器，打开并编辑`app`文件夹里的`CONSTANTS.py`文件。
4. 设置YSGM的地址、服务器和自定义密码，保存
```python
# 设置使用Crepe-Inc-YSGM
YSGM = {
    # 启用状态。若未启用则使用open-command
    'enable': True,
    # MUIP_HOST的api地址，带有/api
    'MUIP_HOST': 'http://127.0.0.1:20011/api',
    'MUIP_TARGET_REGION': 'dev_gio'
}

# 设置登录认证的密码
auth_pwd = 'jixiaob'
```
9. 在项目目录运行
```shell
python manage.py runserver 0.0.0.0:8000
```
即可在8000端口访问到页面。

### 使用
设置CDKey的地址：/cdk_create

进入需要验证密码，即刚刚设置的`auth_pwd`
![创建CDK](image/ScreenShot2.JPG)

可以设置单个CDKey的使用次数

执行的命令可以是give，当然也可以是其他的命令，多条命令用回车隔开。

>使用不同的连接方式需要对应不同的命令！命令不可混用！

如果连接的是Grasscutter，推荐使用 Grasscutter 命令生成工具:
[GrasscutterCommandGenerator](https://github.com/jie65535/GrasscutterCommandGenerator)

如果连接的是MUIP，可以参考以下两个在线命令生成工具：
[https://cmd.d2n.moe/new/](https://cmd.d2n.moe/new/)
[https://gm.casks.me/gm/index.html](https://gm.casks.me/gm/index.html)


生成的个数可以填多个就可以批量生成，但是不要过多。

选择CDK的过期时间（默认为90天后，可以在app/CONSTANTS.py里面更改）

限制每个uid可以兑换的同一个CDK的个数

生成速度取决于服务器性能。


### 高级

1. 设置CDK的默认过期时间。

    创建CDK时如果不想每次都设置一个时间，可以在`CONSTANTS.py`中设置默认过期时间
   ```python
    # 设置CDK默认过期时间（默认为90天）
    CDK_expire_day = 90
    ```
    >这样就会自动计算90天之后的日期，然后自动填写在生成CDK页面的表单上。


2. 设置右上角在线人数缓存时间。
    >右上角的在线人数之前一直都是打开一次页面就请求服务器获取一次，因此极大的拖慢了页面的加载速度。

   >因此在2022/12/7引入缓存机制，默认是60秒之内只请求一次服务器获取真实的服务器在线人数，其余的都将使用缓存，而不是重新请求服务器，使得页面访问速度大大提高。
   
   可以在`CONSTANTS.py`中更改默认的缓存过期时间：
    ```python
    # 设置获取在线人数的缓存时间秒数，时间过短可能导致所有页面加载缓慢和大量的服务器查询人数请求
    # 默认为60秒
    online_cache_time = 60
    ```
   可以将它调大，这样请求服务器获取真实在线人数的频率会更低，但是在线人数的时效性会大幅降低。
   
    也可以把它调小，增加获取在线人数的时效性，但是可能请求服务器获取真实人数的频率会变高。

    当然也可以把它调为0或者负数，这样就和没有缓存一样，每次加载页面都会请求服务器获取真实人数，降低页面响应速度。


3. 不想使用的功能
   
   可能有些提供的功能并不想使用，可以进行如下操作，以远程执行为例：
   
   ①首先修改`templates/用户后台.html`，把里面的按钮使用` {#  #} `引起来，注释掉
   ```html
   {#  <a href="./remote_cmd" class="card-title btn btn-success button-click category-button checked">远程执行</a> #}
   ```
   保存。
   
   ②注释掉可能还不够，有写人可能会猜出地址，还要禁掉对应的路由
   
   修改'djangoProject_genshin_player_backend/urls.py'
   
   在对应的功能的路由前加上`# `注释这一行
   ```python
   # path('remote_cmd', views.remote_cmd),
   ```
   保存。
   
   这样就可以把不想要的功能去掉了。


4. 自定义网页背景图
   
   大家还是喜欢背景图是随机图的多，于是直接提供了一个修改图片地址的设置参数，这样就不用一个个到html里面修改了。
   ```python
   # 设置网页背景图链接，默认是/static/images/bg.jpg文件
   # 也可以设置一些随机图的地址 比如https://api.mtyqx.cn/tapi/random.php
   # 更多随机图地址详见我博客https://blog.jixiaob.cn/?post=93
   background_image = './usr/theme/images/bg.jpg'
   ```
   默认就是/static/images/bg.jpg这个图片文件，
   当然也可以改成一些随机图的地址，比如[https://api.mtyqx.cn/tapi/random.php](https://api.mtyqx.cn/tapi/random.php)
   
   [我博客](https://blog.jixiaob.cn/?post=93) 也分享了一些其他的随机图地址以供参考=w=