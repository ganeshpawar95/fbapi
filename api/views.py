from django.shortcuts import render,redirect
from django.shortcuts import render
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from django.views import View
from django.http import HttpResponse
from rest_framework import status

from facebook_business.api import FacebookAdsApi

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from .models import Post, Adset
from .serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer
from django.http import JsonResponse
import json
# from datetime import datetime
from datetime import date
import dateutil.parser as parser

def campagin(request):
	return render(request,'index.html')


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)



@api_view(['GET'])
def removebg(request):
	if request.method=='GET':
		access_token=request.headers['token']
		print(access_token)
		adds=[]
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
		
		return JsonResponse(data1, safe=False)
	else:
		return HttpResponse('not found')


@api_view(['GET'])
def getadset(request):
	if request.method == 'GET':
		access_token=request.headers['token']
		campaignId = request.GET.get('campignId')

		app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
		app_id = '263805807945856'
		id = 'act_2770121319724389'
		CAMPAIGN_ID = campaignId
		FacebookAdsApi.init(access_token=access_token)
		fields = [
	    'name',
	    'start_time',
	    'end_time',
	    'targeting',
	      ]
		data1=[]
		params = {}
		ads= Campaign(CAMPAIGN_ID).get_ad_sets(
	    	fields=fields,
	    	params=params,
	    	)
		print(ads)
		for i in ads:
			data={
			'id':i['id'],
			'name':i['name'],
			'start_time':i['start_time'],
			'end_time':i['end_time'],
			'targeting':i['targeting'],
			}
			data1.append(data)

		today = date.today()
		for i in data1:
			idss=i['id']
			end_time=i['end_time']
			date1 = (parser.parse(end_time))
			endate=date1.date()
			if endate <= today:
				adsts=Adset.objects.filter(id=idss)
				for adsss in adsts:
					targsts=adsss.targeting
					fields = ['targeting','start_time','end_time']
					params = {
					'targeting':targsts,
					}
					updateadset= AdSet(idss).api_update(
					fields=fields,
					params=params,
					)
					print('update ad set',updateadset)
			else:
				print('date is greter then today date')		
		return Response(data1)
	else:
		return HttpResponse('not found')


@api_view(['GET'])
def create_adset(request):
	if request.method == 'GET':
		access_token=request.headers['token']
		campaignId = request.GET.get('campignId')

		app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
		app_id = '263805807945856'
		id = 'act_2770121319724389'
		CAMPAIGN_ID = campaignId
		FacebookAdsApi.init(access_token=access_token)
		fields = []
		params = {
		  'name': 'My Reach Ad Set',
		  'optimization_goal': 'REACH',
		  'billing_event': 'IMPRESSIONS',
		  'end_time': '2020-5-19T23:43:36-0800',
		  'bid_amount': '2',
		  'daily_budget': 20979,
		  'campaign_id': '23844605998330207',
		  'status': 'PAUSED',
		  'targeting': {'facebook_positions':['feed'],'geo_locations':{'countries':['IN']},'user_os':['iOS']},
		}
		adsets= AdAccount(id).create_ad_set(
		  fields=fields,
		  params=params,
		)
		return Response(adsets)
	else:
		return HttpResponse('not found')


@api_view(['GET'])
def get_adset_by_id(request):
	if request.method == 'GET':
		access_token=request.headers['token']

		adsetId = request.GET.get('adsetId')
		app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
		app_id = '263805807945856'
		ADSET_ID = adsetId
		FacebookAdsApi.init(access_token=access_token)
		fields = ['name','start_time','end_time','targeting']
		params = {}
		ad_set = AdSet(ADSET_ID).api_get(
                fields=fields,
                params=params,
            )
		print(ad_set)
		return Response(ad_set)
	else:
		return HttpResponse('not found')


@api_view(['POST'])
def update_ad_set_date(request):
	if request.method == 'POST':
		print('----------------------------------')
		access_token=request.headers['token']
		
		received_json_data = json.loads(request.body)
		endDate = received_json_data['end_time']
		startDate = received_json_data['start_time']
		print('-----------' + endDate)
		adsetId = request.GET.get('adsetId')
		app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
		app_id = '263805807945856'
		ADSET_ID = adsetId
		FacebookAdsApi.init(access_token=access_token)
		fields = ['start_time','end_time']
		print('><><>>',fields)
		params = {
			'start_time':startDate,
			'end_time':endDate,
		}
		updateadset= AdSet(ADSET_ID).api_update(
				fields=fields,
				params=params,
				)
		print(updateadset)
		return Response(updateadset)
	else:
		return HttpResponse('not found')


@api_view(['POST'])
def update_ad_set_targeting(request):
	if request.method == 'POST':
		print('----------------------------------')
		access_token=request.headers['token']
		received_json_data = json.loads(request.body)
		latitude = received_json_data['lati']
		latitude = float(latitude)
		print(latitude)
		longitude = received_json_data['long']
		longitude = float(longitude)
		print(longitude)
		adsetId = request.GET.get('adsetId')
		app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
		app_id = '263805807945856'
		ADSET_ID = adsetId
		FacebookAdsApi.init(access_token=access_token)
		fields = ['targeting']
		print(fields)
		params = {
		'targeting': {'geo_locations':{'custom_locations':[  
          {  
            "radius":30,
            "latitude":latitude,
            "longitude":longitude
         }]},},
		}
		updateadset= AdSet(ADSET_ID).api_update(
				fields=fields,
				params=params,
				)
		print(updateadset)
		return Response(updateadset)
	else:
		return HttpResponse('not found')


@api_view(['POST'])
def update_ad_set_data(request):
	if request.method == 'POST':
		print('----------------------------------')
		access_token=request.headers['token']
		received_json_data = json.loads(request.body)

		endDate = received_json_data['end_time']
		startDate = received_json_data['start_time']
		print('-----------' + endDate)

		latitude = received_json_data['location']['lati']
		latitude = float(latitude)
		print(latitude)

		longitude = received_json_data['location']['long']
		longitude = float(longitude)
		print(longitude)
		
		adsetId = request.GET.get(int('adsetId'))
		print(adsetId)
		targetings={'targeting': {'geo_locations':{'custom_locations':[  
	        	{  
	            "radius":30,
	            "latitude":latitude,
	            "longitude":longitude
	        }]},},
	        }
		try:
			scrapped_url = Adset.objects.get(id=adsetId)
		except Adset.DoesNotExist:
			scrapped_url = Adset.objects.create(id=adsetId,start_time=startDate,end_time=endDate
			,targeting=targetings)
		app_secret = 'db4b3037cd105cfd23b6032aecd2c3ff'
		app_id = '263805807945856'
		ADSET_ID = adsetId
		FacebookAdsApi.init(access_token=access_token)
		fields = ['start_time','end_time','targeting']
		print(fields)
		params = {
			'start_time':startDate,
			'end_time':endDate,
			'targeting': {'geo_locations':{'custom_locations':[  
	        	{  
	            "radius":30,
	            "latitude":latitude,
	            "longitude":longitude
	        }]},},
		}

		updateadset= AdSet(ADSET_ID).api_update(
				fields=fields,
				params=params,
				)
		print(updateadset)
		return Response(updateadset)
	else:
		return HttpResponse('not found')
