from django.contrib import admin
from .models import CustomUser, Post, Adset, AdsetOrignal


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Adset)
admin.site.register(AdsetOrignal)