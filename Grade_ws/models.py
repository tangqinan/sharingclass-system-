from django.db import models

# Create your models here.
class Hotsearch(models.Model):
    rank = models.IntegerField(primary_key=True)
    href = models.CharField(max_length=255)
    title = models.CharField(max_length=100, db_collation='utf8_general_ci')
