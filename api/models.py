from django.db import models
from jsonfield import JSONField


# Create your models here.
class Post(models.Model):
	appky=models.CharField(max_length = 50)


class Adset(models.Model):
	id=models.IntegerField(primary_key=True)
	name=models.CharField(max_length = 50)
	start_time=models.DateTimeField()
	end_time=models.DateTimeField()
	targeting=JSONField(max_length=200)