from django.db import models

# Create your models here.


class CDKey(models.Model):
    # cdkey的值，一般为12位字母和数字
    key = models.CharField(max_length=16)
    # cdk内容（回车分隔的命令，不带/）
    cdk_value = models.TextField(null=True)
    # 邮件模板（可以设置已经创建好的邮件模板，设置之后将忽略cdk_value）
    mail_template_id = models.IntegerField(default=0)
    # 过期时间
    end_time = models.DateField(default='2022-10-1')
    # 总数（有的cdkey可以重复兑换，默认为1）
    total_num = models.IntegerField(default=1)
    # 已经兑换的数量
    used_num = models.IntegerField(default=0)
    # 设置每个uid可兑换次数
    num_by_uid = models.IntegerField(default=1)


class CDkey_Record(models.Model):
    # cdkey
    key = models.CharField(max_length=16)
    # 兑换时间
    use_time = models.DateTimeField(auto_now=True)
    # 兑换用户uid
    user_uid = models.CharField(max_length=16)


# 记录uid上次签到时间来判断今天是否已签到
class Daily_Sign_Record(models.Model):
    # 最近签到日期
    sign_date = models.DateField(auto_now=True)
    # 签到的uid
    sign_uid = models.CharField(max_length=16)
