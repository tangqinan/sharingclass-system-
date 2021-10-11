# _*_ coding: utf-8 _*_
"""
Time:     2021/6/23 21:31
Author:   Jason_Xue(薛伟-vx：xw809341512)
Version:  V 1.0
File:     submit_msg.py
Describe: 这块主要写后台管理系统
          1、登陆。

"""
from django.http import HttpResponse


from Official_ws import models


def submit_msg_data(request,email):
    try:
        query_set = models.New_entries.objects.all().values('email','time','gene_name','organism','more','read_sum').order_by('-time')
        count = query_set.count()
        # 把submit留言板数据存入read_count
        new_count = models.UserTable.objects.filter(email=email)[0].read_count
        new_count = count - new_count

        return query_set,new_count
    except Exception as e:
        print(e)


def submit_msg_data_update(request):
    try:
        if request.method == "GET":
            email = request.GET.get('email')

            query_set = models.New_entries.objects.all()
            count = query_set.count()
            models.UserTable.objects.filter(email=email).update(read_count=count)

            # 查出所有的字段
            for item in query_set:
                read_sum = models.New_entries.objects.filter(id=item.id)[0].read_sum
                models.New_entries.objects.filter(id=item.id).update(read_sum=read_sum+1)

            return HttpResponse(1)
    except Exception as e:
        print(e)


