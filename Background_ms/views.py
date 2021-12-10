import os
import time

import xlrd
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Background_ms import models
from Official_ws import models as Ofmodels
from Background_ms.models import class_table
from Official_ws.models import UserTable
from Official_ws.models import UserTable
from iClass.settings import BASE_DIR


def index(request):
    return render(request,'Background_ws/index.html')


def cls_table(request):
    return render(request,'Background_ws/cls_table.html')


def cla_info(request):
    return render(request,'Background_ws/cla_info.html')


def photo(request):
    return render(request,'Background_ws/photo.html')

def stu_info(request):
    return render(request,'Background_ws/stu_info.html')

def listdir(path):
    list_name=[]
    for root, dirs, files in os.walk(path):
        list_name.append(files)
    return list_name


def uploadmultiple(request):                   #加一个参数：班级ID
    origin_class_id = request.session.get('origin_class_id', 'None')
    mkpath=os.path.join(BASE_DIR,'static/class_file/'+origin_class_id+'/photo_album')
    files = request.FILES.getlist('photo')
    for rec_file in files:
        t=time.time()
        file_name=str(int(round(t * 1000000)))+'.jpg'
        time.sleep(0.1)
        with open(os.path.join(BASE_DIR,'static/class_file/'+origin_class_id+'/photo_album/'+file_name),'wb') as f:
            f.write(rec_file.read())
            f.flush()

    # 读取文件夹中所有的图片
    path = os.path.join(BASE_DIR, 'static/class_file/'+origin_class_id+'/photo_album')
    list_name = listdir(path)
    filePath=[]
    for i in list_name:
        #j是列表
        for j in i:
            filePath.append('../../static/class_file/'+origin_class_id+'/photo_album/'+j)
    return render(request,'Background_ws/photo.html',{
        'data':filePath,
    })

def uploadusertable(request):
    # 获取文件句柄
    if request.method == 'POST':
        origin_class_id = request.session.get('origin_class_id', 'None')
        class_name = request.session.get('class_name', 'None')
        QQ=request.session.get('QQ','None')
        file_handle = request.FILES.get('file')
        if file_handle:
            # 随机生成文件名
            t = time.time()
            filename = str(int(round(t * 1000000))) + file_handle.name
            # 将文件保存在/Two/files目录下
            # os.path.join把目录和文件合成一个路径
            dir = os.path.join(os.path.join(BASE_DIR,'static/class_file/'+origin_class_id+'/Student_info'), filename)
            destination = open(dir.encode('utf8'), "wb+")
            for chunk in file_handle.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            createUserByExcel(dir,class_name,origin_class_id)
        return render(request, 'Background_ws/index.html',{'QQ':QQ})
    else:
        return render(request,'Background_ws/index.html')


def createUserByExcel(filename,class_name,origin_class_id):
    # 打开文件
    file_xlsx = xlrd.open_workbook(filename)
    all_sheet = file_xlsx.sheets()
    # 获取第一张表
    sheet1 = all_sheet[0]
    # sheet1_name = sheet1.name
    # 获取表的行数，同理sheet1.ncols表的列数，sheet1.name获取表的名字
    sheet1_rows = sheet1.nrows
    for i in range(1, sheet1_rows):
        value_list = []
        t=time.time()
        if sheet1.row_values(i):
            value_list.append(Ofmodels.UserTable(
                class_name=class_name,
                name=sheet1.row_values(i)[0],
                age=sheet1.row_values(i)[1],
                email=sheet1.row_values(i)[2],
                pin=0000,
                level=0,
                password=sheet1.row_values(i)[3],
                origin_class_id=origin_class_id,
                origin_user_id='ID_%s'%int(round((t+1)*1000)),
                is_delete=0,
                # 此处需要注意：models中age为Interge，存储时age要转换成int类型
            ))
        time.sleep(0.1)
        if Ofmodels.UserTable.objects.filter(email=sheet1.row_values(i)[2]).count() == 0:
                Ofmodels.UserTable.objects.bulk_create(value_list)
        else:
            continue

def file_upload(request):
    if request.method == 'POST':
        origin_class_id=request.session.get('origin_class_id','None')
        file_handle = request.FILES.get('file')
        if file_handle:
            t=time.time()
            filename = str(int(round(t * 1000000)))+ file_handle.name
            time.sleep(0.1)
            dir = os.path.join(os.path.join(BASE_DIR,'static/class_file/'+origin_class_id+'/class_table'), filename)
            destination = open(dir.encode('utf8'), "wb+")
            for chunk in file_handle.chunks():
                destination.write(chunk)
            destination.close()
            createClassTableByExcel(dir,origin_class_id)
            data = class_table.objects.filter(Q(class_id=origin_class_id) & Q(is_delete=1))
            context = {
                'DATA': data
            }
            return render(request,'Background_ws/cls_table.html',context=context)
    else:
        return render(request,'Background_ws/cls_table.html')
def createClassTableByExcel(filename,origin_class_id):
    try:
        # 打开文件
        file_xlsx = xlrd.open_workbook(filename)
        all_sheet = file_xlsx.sheets()
        # 获取第一张表
        sheet1 = all_sheet[0]
        # print(sheet1.row_values(1)[1])
        # sheet1_name = sheet1.name
        # 获取表的行数，同理sheet1.ncols表的列数，sheet1.name获取表的名字
        sheet1_rows= sheet1.nrows
        # sheet1_ncols = sheet1.ncols
        value_list = []
        # for i in range(1, sheet1_rows):
        #     if sheet1.row_values(i):
        value_list.append(models.class_table(
        class_id =origin_class_id,
        number_1=sheet1.row_values(1)[1],
        number_2=sheet1.row_values(1)[2],
        number_3=sheet1.row_values(1)[3],
        number_4=sheet1.row_values(1)[4],
        number_5=sheet1.row_values(1)[5],
        number_6=sheet1.row_values(1)[6],
        number_7=sheet1.row_values(1)[7],
        number_8=sheet1.row_values(2)[1],
        number_9=sheet1.row_values(2)[2],
        number_10=sheet1.row_values(2)[3],
        number_11=sheet1.row_values(2)[4],
        number_12=sheet1.row_values(2)[5],
        number_13=sheet1.row_values(2)[6],
        number_14=sheet1.row_values(2)[7],
        number_15=sheet1.row_values(3)[1],
        number_16=sheet1.row_values(3)[2],
        number_17=sheet1.row_values(3)[3],
        number_18=sheet1.row_values(3)[4],
        number_19=sheet1.row_values(3)[5],
        number_20=sheet1.row_values(3)[6],
        number_21=sheet1.row_values(3)[7],
        number_22=sheet1.row_values(4)[1],
        number_23=sheet1.row_values(4)[2],
        number_24=sheet1.row_values(4)[3],
        number_25=sheet1.row_values(4)[4],
        number_26=sheet1.row_values(4)[5],
        number_27=sheet1.row_values(4)[6],
        number_28=sheet1.row_values(4)[7],
        number_29=sheet1.row_values(5)[1],
        number_30=sheet1.row_values(5)[2],
        number_31=sheet1.row_values(5)[3],
        number_32=sheet1.row_values(5)[4],
        number_33=sheet1.row_values(5)[5],
        number_34=sheet1.row_values(5)[6],
        number_35=sheet1.row_values(5)[7],
        ))
        ######################################################### 存储 这里有问题
        # value_dict={} #将value_list列表数据转换为字典数据格式
        data = class_table.objects.filter(class_id=origin_class_id)
        if data.exists():
            data.update(is_delete=0)
            data.bulk_create(value_list)
            return "Up download 'class_table' seccess!"
        else:
            data.bulk_create(value_list)
            return "Up download 'class_table' seccess!"
    except Exception as e:
        print('报错信息',e)
        return e
def download(request):
    file = open(os.path.join(BASE_DIR,'static\com_files\课表.xls'), 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="课表.xls"'
    return response
