from Grade_ws   import views
from django.urls import path

urlpatterns=[
   path('index/',views.index,name='index'),
   path('notice_detail/',views.notice_detail,name='notice_detail'),
   path('notice_list/',views.notice_list,name='notice_list'),
   path('photo_list/',views.photo_list,name='photo_list'),
]