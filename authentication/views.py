from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from . import serializers
from .cognito import Cognito
from .models import User
cognito_obj = Cognito()
# Create your views here.
class LoginView(APIView):
    def post(self, request):
        # --- boto3 처리 부분 --- #
        result = cognito_obj.sign_in(request)
        # --- boto3 처리 부분 종료 --- #

        if(result == -1): # 잘못된 비밀번호
            return JsonResponse({'result' : 'wrong password'})
        elif(result): # 정상 
            return JsonResponse({'result' : 'OK',
            'AccessToken' : result[0],
            'IdToken' : result[1]})
        else: # 회원정보가 존재하지 않는 경우 포함
            return JsonResponse({'result' : 'Fail'})





class RegisterView(APIView):
    def put(self, request):
        # 아이디, 비밀번호, 이메일
        deserializer = serializers.UserSerializer(data = request.data)
        if(deserializer.is_valid()):
            resp = cognito_obj.sign_up(request)
            if(resp):
                return JsonResponse({'result' : 'OK'})
            else:
                return JsonResponse({'result' : 'Fail'})
        


        else: # 이미 존재하는 회원인 경우 포함
            return JsonResponse({'result' : 'invalid'})
    def post(self, request):
            resp = cognito_obj.confirm_sign_up(request)
            if(resp):
                user = User(username = request.data['username'],
                password = request.data['password'],
                email = request.data['email'])
                user.save()

                return JsonResponse({'result' : 'OK'})
            else:
                return JsonResponse({'result' : 'Fail'})


class UserAuthView(APIView):
    def get(self, request):
        resp = cognito_obj.check_user_auth(request)
        if(resp):
            return JsonResponse({'username' : resp})
        else:
            return JsonResponse({'result' : 'Fail'})
