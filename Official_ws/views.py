import hashlib
import time
import random
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Official_ws import models
from Official_ws.GlobeUtils import send_email
# 登录
from Official_ws.models import UserTable
from Official_ws.submit_msg import submit_msg_data
from Official_ws.userCom_msg import userCom_msg_data
def login(request):
    if request.method == "GET":
                res = request.COOKIES
                email = res.get('email', '')
                return render(request, 'Official_ws/login.html', context={'email': email})
    if request.method == "POST":
        email= request.POST.get('email')
        pin = request.POST.get('pin')
        password = request.POST.get('password')
        request.session['email'] = email
        # print(userId,'/',query_set[0].email)
        # if query_set[0].email:
        try:
            query_set = models.UserTable.objects.filter(email=email)
            if password != '':
                # hash_pwd = hashlib.new('md5', hz.encode('utf-8')).hexdigest()
                 if query_set[0].password == password:
                     # 设置session
                     request.session['is_login'] = True
                     request.session['username'] = query_set[0].user_name
                     request.session['level'] = query_set[0].level
                     request.session['email'] = query_set[0].email
                     request.session['password'] = query_set[0].password
                     request.session['user_id'] = query_set[0].user_id
                     request.session['password'] = query_set[0].password
                     request.session['class_id'] = query_set[0].class_id
                     # 设置session关闭浏览器时失效
                     request.session.set_expiry(0)

                     # 登陆成功后更换验证码
                     pin= "".join(random.sample("0123efghjkl456mnopqstuvwsz789abcdef", 4))
                     models.UserTable.objects.filter(email=query_set[0].email).update(pin=pin)
                     # re = redirect('../class_index/')
                     # re.set_cookie('email',query_set[0].email,path='../')
                     # return re
                     QQ = email[0:10]
                     return render(request, 'Grade_ws/index.html',{'QQ':QQ})
                 else:
                     email = request.session.get('email', '')
                     return render(request, 'Official_ws/login.html', {'email': email, 'errormsg': '提示：密码错误！请重新输入'})

            else:
                if pin == query_set[0].pin:
                    # 设置session
                    request.session['is_login'] = True
                    request.session['user_name'] = query_set[0].user_name
                    request.session['level'] = query_set[0].level
                    request.session['email'] = query_set[0].email
                    request.session['user_id'] = query_set[0].user_id
                    request.session['password'] = query_set[0].password
                    request.session['class_id'] = query_set[0].class_id


                    # 设置session关闭浏览器时失效
                    request.session.set_expiry(0)

                    # 登陆成功后更换验证码
                    pin = "".join(random.sample("0123efghjkl456mnopqstuvwsz789abcdef", 4))
                    models.UserTable.objects.filter(email=query_set[0].email).update(pin=pin)
                    # re = redirect('../class_index/')
                    # re.set_cookie('email', query_set[0].email, path='../')
                    # return re
                    QQ=email[0:10]
                    return render(request, 'Grade_ws/index.html',{'QQ',QQ})
                else:
                    email = request.session.get('email', '')
                    return render(request, 'Official_ws/login.html', {'email': email, 'errormsg': '提示：验证码错误！请重新输入'})
        except Exception:
            email= request.session.get('email', '')
            return render(request, 'Official_ws/login.html', {'email': email, 'errormsg': '提示：用户名不存在！请获取验证码进行注册~'})


# 获取验证码
def acquire_code(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        class_id = request.GET.get('class_id')
        pin= "".join(random.sample("0123efghjkl456mnopqstuvwsz789abcdef", 4))
        try:
            query_set = models.UserTable.objects.filter(email=email).values('email')
            print(query_set)
            if list(query_set) ==[]:
                t = time.time()
                hz = 'ID_%s' % int(round(t * 1000))
                hash_pwd = hashlib.new('md5',hz.encode('utf-8')).hexdigest()
                models.UserTable.objects.create(user_id=class_id,email=email,pin=pin,user_name=hz,level='1',password=hash_pwd)
            else:
                models.UserTable.objects.filter(email=email).update(pin=pin)
                print(pin)

            msg = '验证码：<a style="color:#2684b6">' + pin + '</a>,此验证码用于登录“ 共享班级系统。”'
            subject = '【生物信息实验室】'
            back_state = send_email(email, msg, subject)
            if back_state == 0:
                models.UserTable.objects.filter(email=email).update(is_delete=0)
            data = {
                'msg':back_state,
                # 'pin':pin,
            }
            return HttpResponse(content=data)
        except Exception as e:
            print(e)


def index(request):
    is_login = request.session.get('is_login', False)
    if is_login:
        email = request.session.get('email', '')
        QQ=email[0:10]
        return render(request, 'Grade_ws/index.html',{'QQ':QQ})
        # return render(request, 'Official_ws/class_index.html')
    else:
        email = request.session.get('email','')
        return render(request, 'Official_ws/login.html', {'email': email, 'errormsg': '提示：请先登陆再进入系统！'})


def logout(request):
    # 删除session
    request.session.flush()
    return redirect('../login')

def about_us(request):
    return render(request, 'Official_ws/about_us.html')


def courses(request):
    return render(request,'Official_ws/courses.html')


def class_index(request):
    return render(request,'Official_ws/class_index.html')