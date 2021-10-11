from Individual_ws import views
from django.urls import path

urlpatterns=[
   path('index/',views.index,name='index')


]