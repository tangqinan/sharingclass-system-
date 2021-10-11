from django.db import models

# Create your models here.
from django.utils import timezone


class UserInfo(models.Model):
    major = models.CharField(max_length=100, db_collation='utf8_general_ci')
    school = models.CharField(max_length=200, db_collation='utf8_general_ci')
    area = models.CharField(max_length=255, db_collation='utf8_general_ci')
    grade = models.CharField(max_length=20, db_collation='utf8_general_ci')
    student_num = models.IntegerField()


class UserTable(models.Model):
    user_id=models.CharField(max_length=15, db_collation='utf8_general_ci')
    email = models.CharField(max_length=40, db_collation='utf8_general_ci')
    class_id = models.CharField(max_length=15, db_collation='utf8_general_ci')
    pin = models.CharField(max_length=4, db_collation='utf8_general_ci')
    password = models.CharField(max_length=255, default=1)
    level = models.IntegerField(default=1)
    last_login_time = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, db_collation='utf8_general_ci')
    is_delete = models.IntegerField(default=1)


class User_comment(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=50)
    reference = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    read_sum = models.IntegerField(default=1)
    time = models.DateTimeField('保存日期', default=timezone.now)

class New_entries(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField('保存日期',default = timezone.now)
    email = models.EmailField(max_length=50,default='-')
    gene_name = models.CharField(max_length=100,default='-')
    organism = models.CharField(max_length=100,default='-')
    more = models.CharField(max_length=500,default='-')
    read_sum = models.IntegerField(default=1)

