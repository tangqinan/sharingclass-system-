import hashlib
import json
import os
import time
import random

from django.db.models import Q            #引入方便引用filter多条件查询
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from Background_ms import models as BGmodels
from Background_ms.views import listdir
from Grade_ws import models as GRmodels

# Create your views here.
from Official_ws import models
from Official_ws.models import UserTable
from Official_ws.GlobeUtils import send_email
from iClass.settings import BASE_DIR


def login(request):
    if request.method == "GET":
        res = request.COOKIES
        email = res.get('email','')
        return render(request, 'Official_ws/login.html', context={'email': email})
    if request.method == "POST":
        class_name=request.POST.get('class_name')
        email = request.POST.get('email')
        email2=request.POST.get('email2')
        pin = request.POST.get('pin')
        password = request.POST.get('password')
        request.session['email'] = email
        # try

        if password != '':
            query_set = models.UserTable.objects.filter(email=email2)
            if query_set[0].password == password:
                 # 设置session
                 request.session['is_login'] = True
                 request.session['class_name'] = query_set[0].class_name
                 request.session['origin_class_id']=query_set[0].origin_class_id
                 request.session['origin_user_id']=query_set[0].origin_user_id
                 request.session['email'] = query_set[0].email
                 request.session['password'] = query_set[0].password
                 request.session['level'] = query_set[0].level
                 request.session['QQ']=query_set[0].email.split('@')[0]

                 # 设置session关闭浏览器时失效
                 request.session.set_expiry(0)

                 # 登陆成功后更换验证码
                 pin= "".join(random.sample("0123efghjkl456mnopqstuvwsz789abcdef", 4))
                 models.UserTable.objects.filter(email=query_set[0].email).update(pin=pin)
                 QQ=email2.split('@')[0]
                 data = GRmodels.Hotsearch.objects.all()
                 result = data[0:8]
                 origin_class_id = request.session.get('origin_class_id','None')

                 # 数据库id=1为初始表在前端展示
                 if list(BGmodels.class_table.objects.filter(Q(class_id=origin_class_id) & Q(is_delete=1))) != []:
                     classtable_data = BGmodels.class_table.objects.filter(Q(class_id=origin_class_id) & Q(is_delete=1))
                 else:
                     classtable_data = BGmodels.class_table.objects.filter(id=1)

                 # 获取班级相册里面的照片
                 photo_path = os.path.join(BASE_DIR, 'static/class_file/' + origin_class_id + '/photo_album')
                 list_name = listdir(photo_path)
                 if list_name!=[]:
                     filePath = []
                     for i in list_name:
                         for j in i:
                             filePath.append('../../static/class_file/' + origin_class_id + '/photo_album/' + j)
                     file_Path = filePath[-8:]  #取最新的八张照片
                 else:
                     photo_path=os.path.join(BASE_DIR, 'static/Grade_ws/images/portfolio')
                     list_name=listdir(photo_path)
                     filePath = []
                     for i in list_name:
                         for j in i:
                             filePath.append('../../static/Grade_ws/images/portfolio/' + j)
                     file_Path = filePath[-8:]  # 取最新的八张照片
                 level = query_set[0].level
                 if level == 1:
                     return render(request, 'Background_ws/index.html')
                 else:
                     return render(request, 'Grade_ws/index.html',{
                         'QQ':QQ,'result':result,'classtable_data':classtable_data,'file_Path0':file_Path[0],'file_Path1':file_Path[1]
                         , 'file_Path2': file_Path[2],'file_Path3':file_Path[3],'file_Path4':file_Path[4],'file_Path5':file_Path[5]
                         , 'file_Path6': file_Path[6],'file_Path7':file_Path[7]
                                                                   })
            else:
                 email = request.session.get('email', '')
                 return render(request, 'Official_ws/login.html', {'email': email, 'errormsg': '提示：密码错误！请重新输入'})

        else:
            query_set = models.UserTable.objects.filter(email=email)
            if query_set[0].pin == pin:
                # 设置session
                request.session['is_login'] = True
                request.session['class_name'] = query_set[0].class_name
                request.session['origin_class_id'] = query_set[0].origin_class_id
                request.session['origin_user_id'] = query_set[0].origin_user_id
                request.session['email'] = query_set[0].email
                request.session['password'] = query_set[0].password
                request.session['level'] = query_set[0].level
                request.session['QQ']=query_set[0].email.split('@')[0]

                # 设置session关闭浏览器时失效
                request.session.set_expiry(0)
                # 登陆成功后更换验证码
                pin = "".join(random.sample("0123efghjkl456mnopqstuvwsz789abcdef", 4))
                models.UserTable.objects.filter(email=query_set[0].email).update(pin=pin)
                #获取QQ头像
                QQ = email.split('@')[0]
                data = GRmodels.Hotsearch.objects.all()
                result = data[0:8]
                # 获取数据库表中的课程信息
                origin_class_id = request.session.get('origin_class_id', 'None')
                #数据库id=1为初始表在前端展示
                if list(BGmodels.class_table.objects.filter(Q(class_id=origin_class_id) & Q(is_delete=1)))!=[] :
                  classtable_data = BGmodels.class_table.objects.filter(Q(class_id=origin_class_id) & Q(is_delete=1))
                else:
                  classtable_data = BGmodels.class_table.objects.filter(id=1)

                #获取班级相册里面
                photo_path = os.path.join(BASE_DIR, 'static/class_file/' + origin_class_id + '/photo_album')
                list_name = listdir(photo_path)
                if list_name != []:     #第一次出现的八张照片为初始照片
                    filePath = []
                    for i in list_name:
                        for j in i:
                            filePath.append('../../static/class_file/' + origin_class_id + '/photo_album/' + j)
                    file_Path = filePath[-8:]  # 取最新的八张照片
                else:
                    photo_path = os.path.join(BASE_DIR, 'static/Grade_ws/images/portfolio')
                    list_name = listdir(photo_path)
                    filePath = []
                    for i in list_name:
                        for j in i:
                            filePath.append('../../static/Grade_ws/images/portfolio/' + j)
                    file_Path = filePath[-8:]  # 取最新的八张照片
                level=query_set[0].level
                if level==1:
                    return render(request,'Background_ws/index.html',{'QQ': QQ})
                else:
                    return render(request, 'Grade_ws/index.html', {
                        'QQ': QQ, 'result': result, 'classtable_data': classtable_data, 'file_Path0': file_Path[0],
                        'file_Path1': file_Path[1]
                        , 'file_Path2': file_Path[2], 'file_Path3': file_Path[3], 'file_Path4': file_Path[4],
                        'file_Path5': file_Path[5]
                        , 'file_Path6': file_Path[6], 'file_Path7': file_Path[7]
                                                                    })
            else:
                email = request.session.get('email','')
                return render(request, 'Official_ws/login.html', {'email': email, 'errormsg': '提示：验证码错误！请重新输入'})

# 获取验证码
def acquire_code(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        class_name = request.GET.get('class_name')
        pin= "".join(random.sample("0123efghjkl456mnopqstuvwsz789abcdef", 4))
        if len(class_name)<4 or str(class_name.isdigit())=='True' and str(class_name.isalpha())=='True':
            return HttpResponse(json.dumps({
                "msg": 2,
            }))
        else:
            try:
                query_set = models.UserTable.objects.filter(email=email).values('email')
                if list(query_set) == []:
                    t = time.time()
                    hz= 'ID_%s' % int(round(t * 1000))
                    HZ='ID_%s'%int(round((t+1)*1000))
                    hash_pwd = hashlib.new('md5',hz.encode('utf-8')).hexdigest()
                    DIR='static/class_file/'+hz    #班级路径
                    print(DIR)
                    #创建以班级名为主文件夹的俩个子文件夹
                    if models.UserTable.objects.filter(class_name=class_name).count()==0:
                        path='static/class_file'
                        path=os.path.join(path,hz)
                        if not os.path.exists(path):
                            os.makedirs(path)
                            os.makedirs(os.path.join(path,'photo_album'))
                            os.makedirs(os.path.join(path, 'class_table'))
                            os.makedirs(os.path.join(path,'Student_info'))

                        models.ClassDir.objects.create(origin_class_id=hz,class_dir=DIR)
                        models.UserTable.objects.create(class_name=class_name,email=email,pin=pin,password=hash_pwd,level=1,origin_class_id=hz,origin_user_id=HZ  )
                    else:
                        return HttpResponse(json.dumps({
                            "msg": 3,
                        }))
                else:
                    models.UserTable.objects.filter(email=email).update(pin=pin)
                msg = '验证码：<a style="color:#2684b6">' + pin + '</a>,此验证码用于登录“ 共享班级系统。”'
                subject = '【生物信息实验室】'
                back_state = send_email(email, msg, subject)
                return HttpResponse(json.dumps({
                    "msg": back_state,
                }))
            except Exception as e:
                print(e)


def index(request):
    is_login = request.session.get('is_login', False)
    if is_login:
        email = request.session.get('email', '')
        QQ=email.split('@')[0]
        return render(request, 'Grade_ws/index.html',{'QQ':QQ})
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
    return render(request, 'Grade_ws/index.html')