from django.shortcuts import render
from .models import Users, Provinces, Citys, Areas, EmailVerifyRecord
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from cms.check import Base
import json
from utils import email_send
from cms.models import Admin


# Create your views here.
def indexView(request):
    users = Users.objects.filter(is_status=1)
    context = {
        'users': users
    }
    return render(request, 'user/users-list.html', locals())


class AddUserView(View):
    def get(self, request):
        return render(request, 'user/users-add.html')

    def post(self, request):
        nickname = request.POST.get('nickname', None)
        info = Users.objects.filter(nickname=nickname).exists()
        if info:
            return JsonResponse({
                "status": "fail",
                "message": "当前用户已存在",
                "tagid": 'nickname'
            })
        # 增加数据
        Users.objects.create(
            nickname=nickname,
            password=make_password(request.POST.get('password', None)),
            email=request.POST.get('email', None),
            reg_ip=Base.get_ip(request),
            reg_time=Base.getNowTime(request)
        )
        return JsonResponse({
            "status": "success",
            "message": "创建成功",
            "info": ''
        })


class DelUserView(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        Users.objects.filter(id=user_id).update(is_status=0)
        return JsonResponse({
            "status": "success",
            "message": "删除成功",
            "info": ''
        })


class DeltedUserView(View):
    def get(self, request):
        users = Users.objects.filter(is_status=0)
        context = {
            'users': users
        }
        return render(request, 'user/delusers-list.html', locals())

    def post(self, request):
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        print(status)
        if status == 'true':
            Users.objects.filter(id=user_id).update(is_status=1)
            return JsonResponse({
                "status": "success",
                "message": "恢复成功",
                "info": ''
            })
        else:
            Users.objects.filter(id=user_id).delete()
            return JsonResponse({
                "status": "success",
                "message": "删除成功",
                "info": ''
            })


class EditUserView(View):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        # print(user_id)
        info = Users.objects.filter(id=user_id)
        if info:
            users = Users.objects.get(pk=user_id)
            province = Provinces.objects.all()
            context = {
                'users': users,
                'provinces': province
            }
            return render(request, 'user/users-edit.html', context=context)

    def post(self, request):
        # 获取数据
        data = request.POST.get('data', None)
        userid = request.POST.get('user_id', None)

        data = json.loads(data)

        users = Users.objects.get(pk=userid)
        if data['province'] != '':
            users.province = Provinces.objects.get(provinceid=data['province'])
            if data['city'] != '':
                users.city = Citys.objects.get(cityid=data['city'])
                if data['country'] != '':
                    users.country = Areas.objects.get(areaid=data['country'])

        if data['email'] != '':
            users.email = data['email']

        if data['phone'] != '':
            users.phone = data['phone']

        if data['is_student'] != '':
            users.is_student = data['is_student']

        if data['education']:
            users.education = data['education']

        if data['major']:
            users.major = data['major']

        if data['dgree']:
            users.dgree = data['dgree']

        if data['school']:
            users.school = data['school']

        if data['is_status']:
            users.is_status = data['is_status']
        users.save()
        return JsonResponse({
            "status": "success",
            "message": "用户信息更改成功",
            "info": ""
        })


def getCity(request):
    proid = request.GET.get('proid', None)
    info = Citys.objects.filter(provinceid=proid)
    list = []
    for item in info.all():
        list.append([item.cityid, item.city])  # [[xx,xx]]
    return JsonResponse({'data': list})


def getCountoy(request):
    cityid = request.GET.get('cityid', None)
    info = Areas.objects.filter(cityid=cityid)
    list = []
    for item in info.all():
        list.append([item.areaid, item.area])  # [[xx,xx]]
    return JsonResponse({'data': list})


def detailUser(request):
    user_id = request.GET.get('user_id', None)
    user = Users.objects.get(pk=user_id)
    return render(request, 'user/users-detail.html', locals())


class EditPwd(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = Users.objects.get(pk=user_id)
        return render(request, 'user/users-chpwd.html', locals())

    def post(self, request):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        new_pwd = make_password(password=password)
        Users.objects.filter(pk=user_id).update(password=new_pwd)
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


class AvatarUser(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = Users.objects.get(pk=user_id)
        return render(request, 'user/users-avatar.html', locals())

    def post(self, request):
        user_id = request.POST.get('user_id', None)
        users = Users.objects.get(id=user_id)
        avatar = request.FILES.get('avatar')
        try:
            users.avatar = avatar
            users.save()
            data = {'state': 1}
        except:
            data = {'state': 0}
        return JsonResponse(data)


class SendEmal(View):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        users = Users.objects.get(id=user_id)
        context = {
            'users': users,
        }
        return render(request, 'user/send_email.html', context=context)

    def post(self, request):
        user_id = request.POST.get('user_id', None)
        users = Users.objects.get(id=user_id)
        email = users.email
        email_send.send_register_email(email)
        return HttpResponse(110)


def changePwd(request, active_code):
    record = EmailVerifyRecord.objects.filter(code=active_code)
    if record:
        for i in record:
            email = i.email
            users = Users.objects.get(email=email)
            if users:
                return render(request, 'user/pwd_reset.html', {'users': users})


def modiffed(request):
    user_id = request.POST.get('user_id')
    password = request.POST.get('password')
    # print(user_id)
    # print(password)
    new_password = make_password(password=password)
    Users.objects.filter(pk=user_id).update(password=new_password)
    return JsonResponse({
        'status': 'success',
        'message': '密码修改成功',
        'info': ''
    })


# 管理员列表
def managers(request):
    manager = Admin.objects.filter(is_status=1)
    return render(request, 'user/manager.html', locals())


# 编辑管理员姓名
class EditManager(View):
    def get(self, request):
        manager_id = request.GET.get('manager_id')
        manager = Admin.objects.get(pk=manager_id)
        return render(request, 'user/manager-edit.html', context={'manager': manager})

    def post(self, request):
        manager_id = request.POST.get('manager_id')
        manager_name = request.POST.get('manager_name')
        manager = Admin.objects.get(pk=manager_id)
        manager.admin_name = manager_name
        manager.save()
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 重置管理员密码
class RepwdManager(View):
    def get(self, request):
        manager_id = request.GET.get('manager_id')
        manager = Admin.objects.get(pk=manager_id)
        return render(request, 'user/manager-repwd.html', context={'manager': manager})

    def post(self, request):
        manager_id = request.POST.get('manager_id')
        manager_pwd = request.POST.get('manager_pwd')
        Admin.objects.filter(pk=manager_id).update(password=manager_pwd)
        return JsonResponse({
            'status': 'success',
            'message': '修改成功',
            'info': ''
        })


# 添加管理员
class AddManagerView(View):
    def get(self, request):
        return render(request, 'user/manager-add.html')

    def post(self, request):
        manager_name = request.POST.get('manager_name')
        password = request.POST.get('password')
        manager = Admin.objects.filter(admin_name=manager_name).exists()
        if manager:
            return JsonResponse({
                'sutatus': 'fail',
                'message': '用户名已存在',
                'info': manager_name
            })
        Admin.objects.create(admin_name=manager_name, password=password, is_status=1, reg_ip=Base.get_ip(request),
                             reg_time=Base.getNowTime(request))
        return JsonResponse({
            'status': 'success',
            'message': '添加成功',
            'info': manager_name,
        })
def delManager(request):
    manager_id=request.POST.get('manager_id')
    manager=Admin.objects.filter(pk=manager_id).exists()
    if manager:
        Admin.objects.filter(pk=manager_id).update(is_status=0)
        return JsonResponse({
            'status':'success',
            'message':'删除成功',
            'info':''
        })
    else:
        return JsonResponse({
            'status':'fail',
            'message':'删除失败，用户不在',
            'info':''
        })