from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

# Create your views here.
class LoginView(APIView):
    def get(self, request):
        return HttpResponse("login1")

    def post(self, request):
        return HttpResponse("login2")

class RegisterView(APIView):
    def get(self, request):
        return HttpResponse("register1")

    def post(self, request):
        return HttpResponse("register2")

