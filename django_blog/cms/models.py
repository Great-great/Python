from django.db import models


# Create your models here.

class Admin(models.Model):
    admin_name = models.CharField('管理员用户名', max_length=255)
    password = models.CharField('管理员密码', max_length=32)
    reg_time = models.DateTimeField('注册时间', auto_now_add=True)
    reg_ip = models.CharField('注册ip', max_length=255, blank=True, null=True)
    last_time = models.DateTimeField('最后一次登录时间', auto_now=True)
    last_ip = models.CharField('最后一次登录IP', max_length=255, blank=True, null=True)
    is_status = models.BooleanField('是否可用', default=True)

    class Meta:
        verbose_name = '管理员'
        verbose_name_plural = '管理员列表'
        db_table = 'zhouju_admins'
