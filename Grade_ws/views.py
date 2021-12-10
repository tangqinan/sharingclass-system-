from django.shortcuts import render

# Create your views here.
from Grade_ws import models


def index(request):
    data = models.Hotsearch.objects.all()
    result = data[0:8]
    context = {
        'RESULT':result
    }
    print(result)
    return render(request, 'Grade_ws/index.html',context=context)


def notice_detail(request):
    return render(request,'Grade_ws/notice_detail.html')

def notice_list(request):

    return render(request,'Grade_ws/notice_list.html')

def photo_list(request):
    return render(request,'Grade_ws/photo_list.html')