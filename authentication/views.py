from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from . import serializers
from .cognito import Cognito

# Create your views here.
class LoginView(APIView):
    def post(self, request):

        # --- boto3 처리 부분 --- #
        cognito_obj = Cognito() 
        token = cognito_obj.sign_in(request)
        # --- boto3 처리 부분 종료 --- #

        if(token == -1): # 잘못된 비밀번호
            return JsonResponse({'result' : 'wrong password'})
        elif(token): # 정상 
            return JsonResponse({'result' : 'valid request',
            'token' : token})
        else: # 회원정보가 존재하지 않음
            return JsonResponse({'result' : 'No user found'})





class RegisterView(APIView):
    def post(self, request):
        # 아이디, 비밀번호, 이메일
        deserializer = serializers.UserSerializer(data = request.data)
        if(deserializer.is_valid()):
            
            deserializer.save() # User object DB에 저장
            return JsonResponse({'result' : 'valid'})
        else:
            return JsonResponse({'result' : 'invalid'})
            