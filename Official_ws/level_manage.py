# _*_ coding: utf-8 _*_
"""
Time:     2021/6/21 10:30
Author:   Jason_Xue(薛伟-vx：xw809341512)
Version:  V 1.0
File:     level_manage.py
Describe: 这块主要写后台管理系统
          1、这块主要写超级管理员增删改查普通管理员。
"""
import hashlib
import json
import time

from django.core.paginator import Paginator
from django.http import JsonResponse

from Official_ws import models
from Official_ws.GlobeUtils import trans_queryset_toJson


def level_manage_data(request):
    try:
        if request.method == 'GET':
            page = request.GET.get('page')
            limit = request.GET.get('limit')
            query_set = models.UserTable.objects.filter(is_delete=0).values('id', 'name','age','class_name',  'email',
                                                                            'pin','password', 'level','origin_user_id','origin_class_id').order_by('id')
            count = query_set.count()
            paginator = Paginator(query_set, limit)
            query_set = paginator.page(number=page)
            query_set = trans_queryset_toJson(list(query_set), count)
            return JsonResponse(query_set)
    except Exception:
        return


def level_manage_data_save(request):
    try:
        if request.method == 'GET':
            name = request.GET.get('name')
            age = request.GET.get('age')
            class_name = request.GET.get('class_name')
            email = request.GET.get('email')
            pin= request.GET.get('pin')
            password= request.GET.get('password')
            level = request.GET.get('level')
            origin_user_id = request.GET.get('origin_user_id')
            origin_class_id= request.GET.get('origin_class_id')
            query_set = models.UserTable.objects.filter(origin_user_id=origin_user_id)
            print('前',password)
            print('数据库',query_set[0].password)
            hash_pwd = hashlib.new('md5', query_set[0].password.encode('utf-8')).hexdigest()
            if password == hash_pwd:
                password = query_set[0].password

            if level != "0" and level != "1" :
                data = {
                    'msg': '等级：0为超级管理员, 1为普通管理员,请重新选择~'
                }
                return JsonResponse(data)

            query_set.update(name=name, email=email, pin=pin,age=age, level=level,password=password,class_name=class_name,origin_class_id=origin_class_id,origin_user_id=origin_user_id)

            data = {
                'msg': '保存成功！'
            }
            return JsonResponse(data)

    except Exception:
        data = {
            'msg': '保存失败！'
        }
        return JsonResponse(data)


def level_manage_data_delete(request):
    try:
        if request.method == 'GET':
            is_delete = request.GET.get('is_delete')
            print(is_delete)
            origin_user_id = request.GET.get('origin_user_id')
            models.UserTable.objects.filter(origin_user_id=origin_user_id).update(is_delete=is_delete)
            data = {
                'msg': '删除成功！'
            }
            return JsonResponse(data)

    except Exception:
        data = {
            'msg': '删除失败！'
        }
        return JsonResponse(data)

def level_manage_data_add(request):
    if request.method == 'GET':
        try:
            t = time.time()
            hz = 'ID_%s' % int(round(t * 1000))
            origin_class_id= request.GET.get('origin_class_id')
            print(origin_class_id)
            models.UserTable.objects.create(origin_user_id=hz,origin_class_id=origin_class_id,password=123456,pin=0000,
                                            level=1,age=18)
            data = {
                'msg': '创建成功！'
            }
            return JsonResponse(data)

        except Exception:
            print(Exception)
            data = {
                'msg': '创建失败！'
            }
            return JsonResponse(data)



def level_manage_data_del(request):
    try:
        if request.method == "GET":
            origin_user_id = request.GET.get('chose_data')
            for item in json.loads(origin_user_id):
                models.UserTable.objects.filter(origin_user_id=item['origin_user_id']).update(is_delete=0)
                print('删除成功')

            data = {
                'msg': '批量删除成功！'
            }
            return JsonResponse(data)

    except Exception:
        print(Exception)
        data = {
            'msg': '批量删除失败！'
        }
        return JsonResponse(data)


