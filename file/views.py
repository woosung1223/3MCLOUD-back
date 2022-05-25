import uuid
import os
from django.http import FileResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib.parse import urlparse
# from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404, render

AWS_ACCESS_KEY_ID = settings.AWS_S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_S3_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@csrf_exempt
def uploadFile(request):
    if request.method == "POST":
        # 여러개 파일 저장
        uploadedFiles = request.FILES.getlist('files')
        # url = request.POST["url"] # 전체 url
        # file_path = urlparse(url).path.split("/")
        file_path = request.POST["file_path"] # 현재 디렉토리 위치
        print(file_path)
        user_id = "test" #임시 user 생성
        for uploadedFile in uploadedFiles:
            # 예외 처리: 이름 같은 파일 없는지 확인 -> 있으면 추가로 이름 붙여서 저장
            fname, ext = os.path.splitext(str(uploadedFile))
            uuidfilename = str(uuid.uuid1()).replace('-', '')
            # sqlite
            try:
                s3.upload_fileobj(uploadedFile, AWS_STORAGE_BUCKET_NAME, user_id + "/" + file_path + uuidfilename)
            except:
                # 실패 시
                return JsonResponse({
                    'result': 'Upload failed',
                })
    # 파일 업로드 성공
    return JsonResponse({
        'result': 'Upload succeed',
    })

@csrf_exempt
def listFile(request):
    if request.method == 'GET':
        file_path = request.GET["file_path"]
        user_id = request.GET["user"]

        down_path = user_id + "/" + file_path
        paginator = s3.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Prefix=down_path
        )
        file_list = []
        folder_list = []
        try:
            for page in response_iterator:
                for content in page['Contents']:
                    file = content['Key'].strip(down_path)
                    file_split = file.split("/")
                    if (len(file_split)) > 1:
                        if file_split[0] not in folder_list:
                            folder_list.append(file_split[0])
                    else:
                        file_list.append(file_split[0])
        except:
            return JsonResponse({
                'result': 'File not found',
            })

        print("file_list", file_list)
        print("folder_list", folder_list)
        response = {
            'folders': folder_list,
            'files': file_list,
        }
        return JsonResponse(response)


@csrf_exempt
def downloadFile(request, file_id):
    # 버킷에서 찾아서 바로 다운


    s3.download_fileobj(Fileobj, ExtraArgs=None, Callback=None, Config=None)
    # fileobj = 다운로드할 파일류 객체.
    # 버킷: 다운로드할 버킷의 이름
    # 키: 다운로드할 키의 이름 -> user/파일명
    # 버킷 폴더, 받을 object, 다운이름
