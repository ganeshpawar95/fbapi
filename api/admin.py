from django.contrib import admin
from .models import CustomUser, Post, Adset


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Adset)