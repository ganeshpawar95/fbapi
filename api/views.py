from django.shortcuts import render,redirect
from django.shortcuts import render
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from django.views import View
from django.http import HttpResponse
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
import json


# Create your views here.
def removebg(request):
	adds=[]
	access_token = 'EAADv7hN46IABACK043D7oPKJPKAZBK92bRxZAbesb0FRzPX1BFRIgJ7zv2IFo6sH0hI8O1ZA8bha1yZCZAPvLy6biKkF9NwII1gZAZCXsT9BKPBzcPYAspiNvu6zxX6iJDBX6jJR87mYZCjZA5ZAgf5MDKTpEnKFO7cywmBXEjyZBSudJBJ4mNSNAQe0fUY9CinfMgZD'
	app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
	app_id = '263805807945856'
	id = 'act_2770121319724389'
	FacebookAdsApi.init(access_token=access_token)

	fields = [
	  'name',
	  'objective',
	]
	params = {
	  'effective_status': ['ACTIVE','PAUSED'],
	}
	add=AdAccount(id).get_campaigns(
	  fields=fields,
	  params=params)
	return HttpResponse(add)