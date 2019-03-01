from django.db import models
from datetime import datetime

class Users(models.Model):
    # 学历
    EDU_LIST = (
        ('wm', '文盲'),
        ('xx', '小学'),
        ('cz', '初中'),
        ('gz', '高中'),
        ('zz', '中专'),
        ('dz', '大专'),
        ('bk', '本科'),
        ('yjs', '研究生'),
    )
    # 学位
    DGREE_LIST = (
        ('w', '无'),
        ('xs', '学士'),
        ('ss', '硕士'),
        ('bs', '博士'),
    )
    # 重要信息
    nickname = models.CharField("用户名", max_length=255, null=False, unique=True)
    password = models.CharField("密码", max_length=255, blank=False)
    phone = models.CharField("手机", max_length=11, null=True)
    email = models.EmailField("邮箱", max_length=255, null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用 false 不可用
    reg_time = models.DateTimeField("注册时间", null=True)
    reg_ip = models.CharField("注册ip", max_length=255, null=True)
    last_time = models.DateTimeField("最后一次登录时间", null=True)
    last_ip = models.CharField("最后一次登录ip", max_length=255, null=True)
    id_card = models.CharField("身份证号", max_length=255, null=True, unique=True)
    id_name = models.CharField("真实姓名", max_length=255, null=True, unique=False)
    is_student = models.BooleanField("是否报过名", default=False)
    education = models.CharField("学历", choices=EDU_LIST, default="wm", null=True, max_length=11)
    dgree = models.CharField("学位", choices=DGREE_LIST, default="w", null=True, max_length=11)
    address = models.CharField("具体地址", max_length=255, blank=True, null=True)
    major = models.CharField("专业", max_length=255, blank=True, null=True)
    avatar = models.FileField('头像', upload_to='avatars/', null=True)
    school = models.CharField("毕业院校", max_length=255, blank=True, null=True)
    province = models.ForeignKey("Provinces", on_delete=models.CASCADE
                                 , blank=True,
                                 null=True)
    city = models.ForeignKey("Citys", on_delete=models.CASCADE,
                             blank=True, null=True)
    country = models.ForeignKey("Areas", on_delete=models.CASCADE
                                , blank=True, null=True)

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        db_table = "zhouju_users"


# 全国省份
class Provinces(models.Model):
    provinceid = models.CharField("省份id", null=False, max_length=255)
    province = models.CharField("省份名称", max_length=255, null=False)

    class Meta:
        db_table = 'zhouju_provinces'
        verbose_name = "省份名称"
        verbose_name_plural = "全国省份"

    def __str__(self):
        return self.province


# 全国市
class Citys(models.Model):
    cityid = models.CharField("市id", null=False, max_length=255)
    city = models.CharField("市", null=False, max_length=255)
    provinceid = models.CharField("省份id", null=False, max_length=255)

    class Meta:
        db_table = 'zhouju_cities'
        verbose_name = "全国市"
        verbose_name_plural = "城市列表"

    def __str__(self):
        return self.city


# 全国区
class Areas(models.Model):
    areaid = models.CharField("区id", null=False, max_length=255)
    area = models.CharField("区", null=False, max_length=255)
    cityid = models.CharField('市id', null=False, max_length=255)

    class Meta:
        db_table = 'zhouju_areas'
        verbose_name = '全国区'
        verbose_name_plural = '区列表'

    def __str__(self):
        return self.area

#邮箱表
class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register', '注册'),
        ('restart', '找回密码')
    )
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField("类型", choices=send_choices, max_length=10)
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
        db_table = 'zhouju_email'