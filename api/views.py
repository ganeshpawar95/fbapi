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
from array import array


def removebg(request):
	if request.method=='POST':
		access_token=request.GET.get('access_token')
		print(access_token)
		adds=[]
		access_token = access_token
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
		data1=[]
		for i in add:
			data={
			'id':i['id'],
			'name':i['name']
			}
			data1.append(data)
		print(data1)
		
		return JsonResponse(data1)
	else:
		return HttpResponse('not found')