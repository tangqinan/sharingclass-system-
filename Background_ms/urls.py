from Background_ms  import views
from django.urls import path

urlpatterns=[
   path('index/',views.index,name='index'),
   path('cls_table/',views.cls_table,name='cla_table'),
   path('cla_info/',views.cla_info,name='cla_info'),
   path('photo/',views.photo,name='photo'),
   path('stu_info/',views.stu_info,name='stu_info'),
   path('upload_multiple/', views.uploadmultiple, name='uploadmultiple'),
   path('uploadusertable/', views.uploadusertable, name='uploadusertable'),
   path('file_upload/', views.file_upload, name='fileupload'),
   path('download/', views.download, name='download'),
]