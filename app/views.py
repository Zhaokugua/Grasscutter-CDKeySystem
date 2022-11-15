from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from time import sleep
from app.CONSTANTS import *
from app.models import *

# Create your views here.
cdk_list = [x.key for x in CDKey.objects.all()]  # 获取所有key

online_num = get_online()[0]

if not initialize():
    print('服务器连接失败！可能无法正常进行操作！')


def index(request):
    global online_num
    online_num = get_online()[0]
    context = {
        'online_num': online_num
    }
    return render(request, '用户后台.html', context=context)


def cdkey(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        user_uid = request.POST.get('username')
        cdkey_value = request.POST.get('getcdk')
        cdk_obj = CDKey.objects.filter(key=cdkey_value).first()
        if not user_uid:
            context = {
                'message': "请填写uid!	",
                'online_num': online_num,
            }
            return render(request, 'cdkey兑换.html', context=context)
        if cdk_obj:
            if datetime.date.today() > cdk_obj.end_time:
                context = {
                    'message': "兑换码已过期!	",
                    'online_num': online_num,
                }
                return render(request, 'cdkey兑换.html', context=context)
            if cdk_obj.used_num >= cdk_obj.total_num:
                context = {
                    'message': "兑换码已被使用!	",
                    'online_num': online_num,
                }
                return render(request, 'cdkey兑换.html', context=context)
        else:
            context = {
                'message': "无效的兑换码!	",
                'online_num': online_num,
            }
            return render(request, 'cdkey兑换.html', context=context)

        result_list = []
        success = True
        for command in cdk_obj.cdk_value.split('\r\n'):
            flag, res = exec_command(command, uid=user_uid)
            if res['data'] == '玩家不存在。':
                context = {
                    'message': "玩家不存在，请检查uid!	",
                    'online_num': online_num,
                }
                return render(request, 'cdkey兑换.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                }
                return render(request, 'cdkey兑换.html', context=context)
            if not flag:
                success = False
            result_list.append(res['data'])
        if not success:
            context = {
                'message': f"执行兑换时出现异常！请联系管理员！	{str(result_list)}",
                'online_num': online_num,
            }
            return render(request, 'cdkey兑换.html', context=context)
        # 修改兑换码已使用次数
        cdk_obj.used_num += 1
        cdk_obj.save()
        # 记录兑换记录
        used_info = CDkey_Record()
        used_info.key = cdkey_value
        used_info.user_uid = user_uid
        used_info.save()
        context = {
            'message': "兑换成功!	",
            'online_num': online_num,
        }
        return render(request, 'cdkey兑换.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, 'cdkey兑换.html', context=context)


def create_cdkey(request):
    """
    创建cdkey
    可设置cdk的值或者随机生成
    可以批量创建
    设置兑换奖励
    截止时间
    :param request:
    :return:
    """
    global online_num
    online_num = get_online()[0]
    if request.session.get('auth') != 'jixiaob.cn':
        return HttpResponseRedirect('auth')

    if request.method == 'POST':
        cdk_value = request.POST.get('cdk_value')
        end_time = request.POST.get('end_time')
        total_num = request.POST.get('total_num')
        cdk_num = request.POST.get('cdk_num')
        global cdk_list

        new_cdk_list = []
        while len(new_cdk_list) < int(cdk_num):
            cdk_code = generate_code(12)
            while cdk_code in cdk_list:  # 如果已存在就重新生成，直到不存在
                cdk_code = generate_code(12)
            cdk_list.append(cdk_code)
            # 获取信息并生成
            new_cdk = CDKey()
            new_cdk.key = cdk_code
            new_cdk.cdk_value = cdk_value
            # new_cdk.mail_template_id = 1111
            new_cdk.end_time = end_time
            new_cdk.total_num = total_num
            new_cdk.save()
            new_cdk_list.append(cdk_code)
        cdk_str = " ".join(new_cdk_list)
        context = {
            'online_num': online_num,
            'message': f'生成CDK成功！\n{cdk_str}'
        }
        return render(request, '创建cdkey.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, '创建cdkey.html', context=context)


def lucky(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        context = {
            'message': "功能暂未开放!	",
            'online_num': online_num,
        }
        return render(request, '幸运抽奖.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, '幸运抽奖.html', context=context)


def sign(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        context = {
            'message': "功能暂未开放!	",
            'online_num': online_num,
        }
        return render(request, '每日签到.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, '每日签到.html', context=context)


def unlock_map(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        uuid = request.POST.get('uuid')
        if uuid:
            exec_command(f'prop um 1', uuid)
            flag, res = exec_command(f'prop ut 12', uuid)
            if res['data'] == '玩家不存在。':
                context = {
                    'message': "玩家不存在，请检查uid!	",
                    'online_num': online_num,
                }
                return render(request, '解锁深渊.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                }
                return render(request, '解锁深渊.html', context=context)
            context = {
                'message': "解锁成功!	",
                'online_num': online_num,
            }
            return render(request, '解锁深渊.html', context=context)
        else:
            context = {
                'message': "请填写uid!	",
                'online_num': online_num,
            }
            return render(request, '解锁深渊.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, '解锁深渊.html', context=context)


def set_world_level(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        uuid = request.POST.get('uuid')
        level = request.POST.get('level')
        if uuid:
            flag, res = exec_command(f'prop wl {level}', uuid)
            if res['data'] == '玩家不存在。':
                context = {
                    'message': "玩家不存在，请检查uid!	",
                    'online_num': online_num,
                }
                return render(request, '设置世界等级.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                }
                return render(request, '设置世界等级.html', context=context)
            context = {
                'message': "设置成功!	",
                'online_num': online_num,
            }
            return render(request, '设置世界等级.html', context=context)
        else:
            context = {
                'message': "请填写uid!	",
                'online_num': online_num,
            }
            return render(request, '设置世界等级.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, '设置世界等级.html', context=context)


def auth(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        pwd = request.POST.get('password')
        if pwd == auth_pwd:
            request.session['auth'] = 'jixiaob.cn'
            return HttpResponseRedirect('./cdk_create')
        else:
            context = {
                'message': '认证失败！',
                'online_num': online_num
            }
            return render(request, '登录认证.html', context=context)
    context = {
        'online_num': online_num
    }
    return render(request, '登录认证.html', context=context)
