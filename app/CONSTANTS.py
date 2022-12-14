"""
@FILE_NAME : CONSTANTS
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/10/11 9:40
"""
import requests
import random
import datetime
import hashlib
import base64
import json
# 设置服务器open-command的token
Server_token = 'token_value'

# 设置服务器地址，后面不带/
Server_addr = 'https://127.0.0.1'

# 设置MeaMail插件的邮件模板文件夹（暂不需要）
MeaMail_addr = r'plugins\MeaMailPlus\template'

# 邮件默认过期时间戳（默认为邮件发送时间+30天）
Mail_default_expire_time = int((datetime.datetime.now() + datetime.timedelta(days=30)).timestamp())

# 设置CDK默认过期时间（默认为90天）
CDK_expire_day = 90

# 设置网页背景图链接，默认是/static/images/bg.jpg文件
# 也可以设置一些随机图的地址 比如https://api.mtyqx.cn/tapi/random.php
# 更多随机图地址详见我博客https://blog.jixiaob.cn/?post=93
background_image = './usr/theme/images/bg.jpg'

# 设置获取在线人数的缓存时间秒数，时间过短可能导致所有页面加载缓慢和大量的服务器查询人数请求
# 默认为1分钟
online_cache_time = 60

# 设置使用Crepe-Inc-YSGM（MUIP方法）
YSGM = {
    # 启用状态。若未启用则使用open-command
    'enable': False,
    # MUIP_HOST的api地址，带有/api
    'MUIP_HOST': 'http://127.0.0.1:54321/api',
    'MUIP_TARGET_REGION': 'dev_test'
}

# 设置登录认证的密码
auth_pwd = 'jixiaob'


def YSGM_api(cmd, uid=None, msg=None):
    if YSGM['enable']:
        params = {
            'cmd': f'{cmd}',
            'region': YSGM['MUIP_TARGET_REGION'],
            'ticket': f'YSGM@{int(datetime.datetime.now().timestamp())}'
        }
        if uid:
            params['uid'] = uid
        if msg:
            params['msg'] = msg
        sha256_salt = '1d8z98SAKF98bdf878skswa8kdjfy1m9dses'
        query_string = '&'.join([f'{x}={params[x]}' for x in params])
        sha256_result = hashlib.sha256((query_string+sha256_salt).encode('utf8')).hexdigest()
        params['sign'] = sha256_result
        return params
    else:
        print('未开启YSGM！')
        return False


def YSGM_mail(uid, title, sender='PAIMON', expire_time=Mail_default_expire_time, content='This is a Mail.', item_list=None, is_collectible=False):
    """
    生成发送邮件的编码
    uid=235078418&
    title=test&
    content=nyan&
    sender=YSGM&
    expire_time=1669215550&
    is_collectible=False&
    importance=&
    config_id=&
    item_limit_type=2&
    tag=&
    source_type=&
    item_list=&
    cmd=1005
    &region=dev_gio&
    ticket=YSGM%401668616882&
    sign=9529ea7646fcf8551a0aed72e93125e8b71cd3ceb8613c1ab01bbc1a48ddedea
    :param uid: 要发给的用户的uid
    :param title: 邮件标题
    :param sender: 发送者，默认为PAIMON
    :param expire_time: 过期时间，默认为发送邮件后30天
    :param content: 正文内容，默认为'This is a Mail.'
    :param item_list: 物品列表，默认为空
    item_list = [
        {
            'item_id': 11101,    # 物品id
            'amount': 1,         # 数量
            'level': 90,         # 等级
            'promote_level': 0,  # 突破等级
        },
        {
            'item_id': 11201,  # 物品id
            'amount': 3,  # 数量
            'level': 56,  # 等级
            'promote_level': 1,  # 突破等级
        },
    ]
    :param is_collectible: 是否可以收藏，默认为否
    :return: 返回生成后的字符串
    """
    if item_list:
        item_str = ','.join([f'{x.item_id}:{x.amount}:{x.level}:{x.promote_level}' for x in item_list])
    else:
        item_str = ''
    mail_json = {
        'uid': f'{uid}',
        'title': title,
        'sender': sender,
        'expire_time': f'{expire_time}',
        'content': content,
        'item_list': item_str,
        'is_collectible': is_collectible,
    }
    b64_res = base64.b64encode(bytes(json.dumps(mail_json, ensure_ascii=False, separators=(',', ':')), encoding='utf8'))
    return str(b64_res, encoding='utf8')


def initialize():
    if YSGM['enable']:
        # 1101获取服务器人数状态
        params = YSGM_api(1101)

        req_url = YSGM['MUIP_HOST']

        try:
            res = requests.get(req_url, params=params)
            result = res.json()
            if result['msg'] == 'succ' and result['retcode'] == 0:
                # {'gameserver_player_num': {'809.2.1.1': 0}, 'internal_data': 0, 'online_player_num_except_sub_account': 0}
                print('YSGM连接成功！')
                return True
            else:
                print(f'连接服务器失败！请检查配置信息！msg: {result["msg"]}, retcode: {result["retcode"]}')
                return False
        except:
            print('连接服务器失败！请检查运行状态是否正常！')
            return False

    # 测试是否已启用插件
    req_url = f'{Server_addr}/opencommand/api'
    json_ping = {
        'action': 'ping',
    }
    try:
        res_ping = requests.post(req_url, verify=False, json=json_ping)
    except:
        print('连接服务器失败！')
        return False
    if res_ping.status_code != 200:
        if res_ping.status_code == 404:
            print('open-command插件未启用！')
        else:
            print('open-command插件启动异常！')
        return False
    else:
        ping_result = res_ping.json()
        if ping_result['retcode'] == 200 and ping_result['message'] == 'Success':
            print('已检测到open-command插件。')
        else:
            print(f'open-command插件连接失败！{str(ping_result)}')
            return False

    json_server = {
        'action': 'server',
        'token': Server_token
    }
    res_ping = requests.post(req_url, verify=False, json=json_server).json()
    if res_ping['retcode'] != 403:
        print('暂不支持多服务器！')
        return False

    json_test = {
        'action': 'command',
        'token': Server_token,
        'data': 'list uid',
    }
    res_test = requests.post(req_url, verify=False, json=json_test).json()
    if res_test['retcode'] != 200:
        if res_test['retcode'] == 401:
            print('opencommand token认证失败！')

        else:
            print('opencommand 未知错误')
            return False
    else:
        print('opencommand 登录成功！')
        return True


# 获取在线人数的缓存，加速短时间内获取在线人数的速度，减少请求服务器的速度
online_cache = (datetime.datetime.now(), 0)


def get_online():
    global online_cache
    if datetime.datetime.now() - online_cache[0] < datetime.timedelta(seconds=online_cache_time):
        return online_cache[1], None

    if YSGM['enable']:
        params = YSGM_api(1101)
        req_url = YSGM['MUIP_HOST']

        try:
            res = requests.get(req_url, params=params)
            result = res.json()
            if result['msg'] == 'succ' and result['retcode'] == 0:
                # {'gameserver_player_num': {'809.2.1.1': 0}, 'internal_data': 0, 'online_player_num_except_sub_account': 0}
                # 暂时用这个人数看看对不对
                total_num = result['data']['online_player_num_except_sub_account']
                # 更新缓存
                online_cache = (datetime.datetime.now(), total_num)
                return total_num, None
            else:
                return 0, 'Error'
        except:
            return 0, 'Error'

    req_url = f'{Server_addr}/status/server'
    try:
        res_online = requests.get(req_url, verify=False).json()['status']['playerCount']
        # 更新缓存
        online_cache = (datetime.datetime.now(), res_online)
        return res_online, None
    except:
        return 0, 'Error'

    # req_url = f'{Server_addr}/opencommand/api'
    # json_online = {
    #     'action': 'online',
    # }
    # res_online = requests.post(req_url, json=json_online)
    # if res_online.status_code != 200:
    #     print('open-command插件状态异常！')
    #     return False
    # else:
    #     online_result = res_online.json()
    #     if online_result['retcode'] == 200 and online_result['message'] == 'Success':
    #         u_count, u_list = online_result['data']['count'], online_result['data']['playerList']
    #         # print(f'获取在线用户成功！\n当前在线人数{u_count}：{str(u_list)}')
    #         return u_count, u_list
    #     else:
    #         print(f'open-command插件连接失败！{str(online_result)}')
    #         return False


def generate_code(code_len=6):
    all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJIKOLP'
    index = len(all_char) - 1
    code = ''
    for _ in range(code_len):
        num = random.randint(0, index)
        # print(num)
        code += all_char[num]
    return code.upper()


def exec_command(command, uid=None):
    # 执行命令没写转换
    # 所以如果生成cdk的时候用的命令是gc的，执行的时候一定不要改成GM的！
    command = command[1:] if command.startswith('/') or command.startswith('!') else command
    if YSGM['enable']:

        # 如果填写了uid，判断uid是否为纯数字（官端应该只有纯数字uid）
        # 防止兑换cdk的时候uid加字母卡多次兑换bug
        if uid:
            if not uid.isdigit():
                return False, {'data': 'uid不是纯数字！'}

        params = YSGM_api(1116, uid=uid, msg=command)
        req_url = YSGM['MUIP_HOST']
        try:
            res = requests.get(req_url, params=params)
            result = res.json()
            if result['msg'] == 'succ' and result['retcode'] == 0:
                print('YSGM命令执行成功！')
                return True, result
            else:
                print('YSGM命令执行失败！')
                result['data'] = '执行失败，可能是玩家未上线' if not result['data'] else result['data']
                return False, result
        except BaseException as e:
            print('YSGM命令执行失败！')
            print(e)
            return False, {'data': '请求错误，检查服务器'}

    if uid:
        command = command + f' @{uid}'
    req_url = f'{Server_addr}/opencommand/api'
    json_exec = {
        'action': 'command',
        'token': Server_token,
        'data': command,
    }
    res_exec = requests.post(req_url, verify=False, json=json_exec).json()
    if res_exec['retcode'] != 200:
        res_exec['data'] = '' if not res_exec['data'] else res_exec['data']
        print('opencommand 命令执行异常！')
        return False, res_exec
    else:
        print('opencommand 命令执行成功！')
        print(command)
        print(res_exec)
        if res_exec['data'] == '玩家不存在。':
            return False, res_exec
        if '当前目标离线' in res_exec['data']:
            return False, res_exec
        return True, res_exec
