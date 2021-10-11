from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'Grade_ws/index.html')