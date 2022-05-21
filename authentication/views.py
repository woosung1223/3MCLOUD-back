from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from . import serializers
from .cognito import Cognito
from .models import User

# Create your views here.
class LoginView(APIView):
    def post(self, request):
        cognito_obj = Cognito()
        # --- boto3 처리 부분 --- #
        token = cognito_obj.sign_in(request)
        # --- boto3 처리 부분 종료 --- #

        if(token == -1): # 잘못된 비밀번호
            return JsonResponse({'result' : 'wrong password'})
        elif(token): # 정상 
            return JsonResponse({'result' : 'valid request',
            'token' : token})
        else: # 회원정보가 존재하지 않는 경우 포함
            return JsonResponse({'result' : 'Failed'})





class RegisterView(APIView):
    def post(self, request):
        # 아이디, 비밀번호, 이메일
        deserializer = serializers.UserSerializer(data = request.data)
        if(deserializer.is_valid()):
            cognito_obj = Cognito()
            resp = cognito_obj.sign_up(request)
            if(resp):
                return JsonResponse({'result' : 'OK'})
            else:
                return JsonResponse({'result' : 'Failed'})
        


        else: # 이미 존재하는 회원인 경우 포함
            return JsonResponse({'result' : 'invalid'})
    def put(self, request):
            cognito_obj = Cognito()
            resp = cognito_obj.confirm_sign_up(request)
            if(resp):
                user = User(username = request.data['username'],
                password = request.data['password'],
                email = request.data['email'])
                user.save()

                return JsonResponse({'result' : 'OK'})
            else:
                return JsonResponse({'result' : 'Failed'})