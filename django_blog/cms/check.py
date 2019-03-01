from django.views import View
import re
from django.utils import timezone


# 创建一个基类
class Base(View):
    # 获取当前时间
    def getNowTime(request):
        info_time = timezone.now()
        return info_time

    # 验证用户是否登录
    def checkUserLogin(request):
        if request.session.get('admin_name', None):
            return True
        else:
            return False

    # 获取用户ip
    def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        return ip

    # 对数据进行验证
    def check_data(name, pwd):
        # 创建一个字典
        res = {
            'name': None,
            'pwd': None,
            'errors': None,
        }
        # 用户名规则6-15位，包含数字字母,一字母开头
        name_re = re.compile(r'^[a-zA-Z](?=\w*[a-zA-Z])(?=\w*[0-9])\w{5,14}$')
        # 密码同用户名一样
        pwd_re = re.compile(r'^[a-zA-Z](?=\w*[a-zA-Z])(?=\w*[0-9])\w{5,14}$')
        res['name'] = name_re.match(name)
        res['pwd'] = pwd_re.match(pwd)
        if res['name'] == None or res['pwd'] == None:
            res['errors'] = '用户名或密码输入有误！！！'
        return res
