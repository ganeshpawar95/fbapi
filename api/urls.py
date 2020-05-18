from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  url
import json

urlpatterns = [
    path('campagin',campagin,name='campagin'),

	path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),

    path('get_campagin/',removebg,name='getcampagin'),

    path('get_ad_set/',getadset,name='getadset'),
    path('create_adset/',create_adset,name='create_adset'),

    path('get_adset_by_id/',get_adset_by_id,name='get_adset_by_id'),

    path('update_ad_set_date',update_ad_set_date,name='update_ad_set_date'),
    path('update_ad_set_targeting',update_ad_set_targeting,name='update_ad_set_targeting'),
    path('update_ad_set_data',update_ad_set_data,name='update_ad_set_data'),

    path('updated_adset',updated_adset,name='updated_adset')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

