from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  url
import json

urlpatterns = [
    path('get_campagin/',removebg,name='getcampagin'),
    path('campagin',campagin,name='campagin'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

