from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from cms.check import Base
from .models import Admin


# Create your views here.


class Index(Base):
    def get(self, request):
        # 判断用户是否登录
        admin_id = request.GET.get('id')
        status_login = Base.checkUserLogin(request)
        if status_login and admin_id:
            # # 获取ip和时间
            # ip = Base.get_ip(request)
            # info_time = Base.getNowTime(request)
            # 根据IP获取用户
            admin = Admin.objects.get(pk=admin_id)
            # 将数据传递前台
            context = {
                'admin': admin
            }
            return render(request, 'cms/index.html', locals())
        else:
            request.session.flush()
            return redirect('/cms/login/')

    def post(self):
        pass


class Login(Base):
    def get(self, request):
        # 判断用户是否登录：
        login_status = Base.checkUserLogin(request)
        if login_status:
            return redirect('/cms/index/')
        else:
            return render(request, 'cms/login.html')

    def post(self, request):
        # 接收前台数据
        check_name = request.POST.get('admin_name')
        check_pwd = request.POST.get('pwd')
        # 对数据进行校验
        check_status = Base.check_data(check_name, check_pwd)
        # 判断用户名是否注册
        info = Admin.objects.filter(admin_name=check_name).exists()
        if info and check_status['errors'] is None:
            if Admin.objects.get(admin_name=check_name).password == check_pwd:
                ip = Base.get_ip(request)
                info = Admin.objects.get(admin_name=check_name)
                info.last_ip = ip
                info.last_time = Base.getNowTime(request)
                info.save()
                request.session['admin_name'] = check_name
                # print('/cms/index/?id=' + str(info.id))
                return JsonResponse({
                    'status': 'success',
                    'message': '登录成功，可以跳转后台页面',
                    'info': '/cms/index/?id=' + str(info.id),
                })
            else:
                return JsonResponse({
                    'status': 'fail',
                    'message': '密码错误',
                    'info': ''
                })
        elif not info:
            return JsonResponse({
                'status': 'fail',
                'message': '用户名不存在',
                'info': ''
            })
        elif check_status['errors']:
            return JsonResponse({
                'status': 'fail',
                'message': check_status['errors'],
                'info': ''
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'message': '存在不可预知的错误',
                'info': ''
            })


class Logout(Base):
    def get(self, request):
        request.session.flush()  # 删除Session
        return redirect('/cms/login/')
