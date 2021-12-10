from django.db import models

# Create your models here.
from django.utils import timezone



class UserTable(models.Model):
    class_name = models.CharField(max_length=255,db_collation='utf8_general_ci')
    name=models.CharField(max_length=255,db_collation='utf8_general_ci',null=True, blank=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=40, db_collation='utf8_general_ci')
    pin = models.CharField(max_length=4, db_collation='utf8_general_ci')
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    origin_user_id = models.CharField(max_length=255, db_collation='utf8_general_ci')
    origin_class_id = models.CharField(max_length=255, db_collation='utf8_general_ci')
    is_delete = models.IntegerField(default=0)
    last_login_time = models.DateTimeField(auto_now_add=True)


class ClassDir(models.Model):
    origin_class_id = models.CharField(primary_key=True, max_length=255, db_collation='utf8_general_ci')
    class_dir = models.CharField(max_length=255, db_collation='utf8_general_ci')
