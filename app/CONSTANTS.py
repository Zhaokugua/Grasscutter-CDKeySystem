"""
@FILE_NAME : CONSTANTS
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/10/11 9:40
"""
import requests
import random
# 设置服务器open-command的token
Server_token = 'token_value'

# 设置服务器地址，不带http和/
Server_addr = 'https://127.0.0.1'

# 设置MeaMail插件的邮件模板文件夹（暂不需要）
MeaMail_addr = r'plugins\MeaMailPlus\template'

# 设置登录认证的密码
auth_pwd = 'jixiaob'


def initialize():
    # 测试是否已启用插件
    req_url = f'{Server_addr}/opencommand/api'
    json_ping = {
        'action': 'ping',
    }
    res_ping = requests.post(req_url, verify=False, json=json_ping)
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


def get_online():
    req_url = f'{Server_addr}/status/server'
    res_online = requests.get(req_url, verify=False).json()['status']['playerCount']
    return res_online, None
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


def exec_command(command):
    command = command[1:] if command.startswith('/') or command.startswith('!') else command
    req_url = f'{Server_addr}/opencommand/api'
    json_exec = {
        'action': 'command',
        'token': Server_token,
        'data': command,
    }
    res_exec = requests.post(req_url, verify=False, json=json_exec).json()
    if res_exec['retcode'] != 200:
        print('opencommand 命令执行异常！')
        return False, res_exec
    else:
        print('opencommand 命令执行成功！')
        print(command)
        print(res_exec)
        return True, res_exec
