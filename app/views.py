from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from time import sleep
from app.CONSTANTS import *
from app.models import *

# Create your views here.

online_num = get_online()[0]

if not initialize():
    print('服务器连接失败！可能无法正常进行操作！')


def index(request):
    global online_num
    online_num = get_online()[0]
    context = {
        'online_num': online_num,
        'bg_url': background_image,
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
                'bg_url': background_image,
            }
            return render(request, 'cdkey兑换.html', context=context)
        if cdk_obj:
            if datetime.date.today() > cdk_obj.end_time:
                context = {
                    'message': "兑换码已过期!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, 'cdkey兑换.html', context=context)
            if cdk_obj.used_num >= cdk_obj.total_num:
                context = {
                    'message': "兑换码已被使用!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, 'cdkey兑换.html', context=context)
        else:
            context = {
                'message': "无效的兑换码!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, 'cdkey兑换.html', context=context)

        # 判断每个用户的使用次数
        used_times = len(CDkey_Record.objects.filter(user_uid=user_uid).filter(key=cdkey_value))

        if used_times >= cdk_obj.num_by_uid:
            context = {
                'message': "同一个兑换码单个uid使用次数达到上限!	",
                'online_num': online_num,
                'bg_url': background_image,
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
                    'bg_url': background_image,
                }

                return render(request, 'cdkey兑换.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }

                return render(request, 'cdkey兑换.html', context=context)
            if not flag:
                success = False
            result_list.append(res['data'])
        if not success:
            context = {
                'message': f"执行兑换时出现异常！请联系管理员！	{str(result_list)}",
                'online_num': online_num,
                'bg_url': background_image,
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
            'bg_url': background_image,
        }

        return render(request, 'cdkey兑换.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image
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
    # 配置文件可以设置兑换码的默认过期时间，默认90天过期
    default_time = str(datetime.date.today() + datetime.timedelta(days=CDK_expire_day))
    if request.session.get('auth') != 'jixiaob.cn':
        return HttpResponseRedirect('auth')

    cdk_list = [x.key for x in CDKey.objects.all()]  # 获取所有key

    if request.method == 'POST':
        cdk_value = request.POST.get('cdk_value')
        end_time = request.POST.get('end_time')
        total_num = request.POST.get('total_num')
        cdk_num = request.POST.get('cdk_num')
        num_by_uid = request.POST.get('num_by_uid')

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
            new_cdk.num_by_uid = num_by_uid
            new_cdk.save()
            new_cdk_list.append(cdk_code)
        cdk_str = " ".join(new_cdk_list)
        context = {
            'online_num': online_num,
            'message': f'生成CDK成功！\n{cdk_str}',
            'default_time': default_time,
            'bg_url': background_image,

        }
        return render(request, '创建cdkey.html', context=context)
    context = {
        'online_num': online_num,
        'default_time': default_time,
        'bg_url': background_image,
    }
    return render(request, '创建cdkey.html', context=context)


def lucky(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        # 从前端获取用户uid
        uuid = request.POST.get('uuid')
        # 可以用exec_command随机执行一个命令来获取抽奖奖励，用户离线时可以用邮件命令发送奖励
        # 然后context的message显示随机到的抽奖结果返回到页面上显示
        # 例：
        # # 记录随机命令列表
        # command_list = [
        #     '/give 202 x1000',
        #     '/give 201 x100',
        #     '/give 223 x10'
        # ]
        # # 记录命令对应的结果
        # result_list = [
        #     '100摩拉',
        #     '100原石',
        #     '10纠缠之缘'
        # ]
        # # 随机选取
        # random_result = ramdom.randint(0, len(command_list))
        # exec_command(command_list[random_result], uuid)   # give命令需要玩家在线
        # context = {
        #     'message': f"抽奖成功！获得{result_list[random_result]}！",
        #     'online_num': online_num,
        # }
        context = {
            'message': "功能暂未开放!	",
            'online_num': online_num,
            'bg_url': background_image,
        }
        return render(request, '幸运抽奖.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image,
    }
    return render(request, '幸运抽奖.html', context=context)


def sign(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        # 从前端获取用户uid
        uuid = request.POST.get('uuid')

        if not uuid:
            context = {
                'message': "请填写uid！",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '每日签到.html', context=context)

        # 判断数据库里是否有记录和今天是否已经签到
        user = Daily_Sign_Record.objects.filter(sign_uid=uuid).first()
        if user:
            if user.sign_date == datetime.date.today():
                context = {
                    'message': "你今天已经签到过了哦！",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, '每日签到.html', context=context)
        else:
            user = Daily_Sign_Record(sign_uid=uuid)
        # 可以用exec_command执行一个命令来获取签到奖励，用户离线时可以用邮件命令发送奖励
        # 然后context的message显示签到结果返回到页面上显示
        # 然后写到数据库记录一下今天已签到
        flag, res = exec_command('/give 202 x1000', uuid)   # give命令需要玩家在线
        if not flag:
            context = {
                'message': f"执行兑换时出现异常！请联系管理员！	{str(res['data'])}",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '每日签到.html', context=context)
        # 成功了就更新一下表，表示今天签到了
        user.save()
        # 返回信息
        context = {
            'message': "签到成功！获得1000摩拉！",
            'online_num': online_num,
            'bg_url': background_image,
        }
        return render(request, '每日签到.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image
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
                    'bg_url': background_image,
                }
                return render(request, '解锁深渊.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, '解锁深渊.html', context=context)
            context = {
                'message': "解锁成功!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '解锁深渊.html', context=context)
        else:
            context = {
                'message': "请填写uid!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '解锁深渊.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image,
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
                    'bg_url': background_image,
                }
                return render(request, '设置世界等级.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, '设置世界等级.html', context=context)
            context = {
                'message': "设置成功!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '设置世界等级.html', context=context)
        else:
            context = {
                'message': "请填写uid!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '设置世界等级.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image,
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
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '登录认证.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image,
    }
    return render(request, '登录认证.html', context=context)


def remote_cmd(request):
    global online_num
    online_num = get_online()[0]
    if request.method == 'POST':
        uuid = request.POST.get('uuid')
        command = request.POST.get('command')
        if uuid:
            flag, res = exec_command(f'{command}', uuid)
            if res['data'] == '玩家不存在。':
                context = {
                    'message': "玩家不存在，请检查uid!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, '远程执行.html', context=context)
            if '当前目标离线' in res['data']:
                context = {
                    'message': "当前玩家离线，请上线后再执行!	",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, '远程执行.html', context=context)
            if not flag:
                context = {
                    'message': f"执行命令时出现异常！请检查命令格式！	{str(res)}",
                    'online_num': online_num,
                    'bg_url': background_image,
                }
                return render(request, '远程执行.html', context=context)
            context = {
                'message': "执行命令成功!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '远程执行.html', context=context)
        else:
            context = {
                'message': "请填写uid!	",
                'online_num': online_num,
                'bg_url': background_image,
            }
            return render(request, '远程执行.html', context=context)
    context = {
        'online_num': online_num,
        'bg_url': background_image,
    }
    return render(request, '远程执行.html', context=context)
