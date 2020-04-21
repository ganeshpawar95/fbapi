from django.db import models

# Create your models here.
class Post(models.Model):
	appky=models.CharField(max_length = 50)