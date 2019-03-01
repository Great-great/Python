from random import Random
from django.core.mail import send_mail

from user.models import EmailVerifyRecord
from django_blog.settings import EMAIL_FROM



def random_str(random_length=8):
    '''生成随机字符串'''
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type='restart'):
    '''发送注册邮件'''
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    code=random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # EmailVerifyRecord.objects.create(code=code,email=email,send_type=send_type)

    # 定义邮件内容
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "注册链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/user/active/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
    if send_type == "restart":
        email_title = "重置密码链接"
        email_body = "请点击下面的链接重置你的密码 : http://127.0.0.1:8000/user/active/{0}".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass