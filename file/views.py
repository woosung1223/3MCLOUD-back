import uuid
import os
from django.http import FileResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib.parse import urlparse

# from django.contrib.auth.models import AbstractUser

AWS_ACCESS_KEY_ID = settings.AWS_S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_S3_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
AWS_REGION = settings.AWS_REGION
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@csrf_exempt
def uploadFile(request):
    if request.method == "POST":
        # 여러개 파일 저장
        uploadedFiles = request.FILES.getlist('files')
        if len(uploadedFiles) == 0:
            return JsonResponse({
                'result': 'file not found',
            })
        # compression = request.POST['compression']
        # isAudio = request.POST['isAudio']

        file_path = request.POST["file_path"]  # 현재 디렉토리 경로
        user_id = request.POST["user_id"]  # 임시 user 생성
        for uploadedFile in uploadedFiles:
            # 예외 처리: 이름 같은 파일 없는지 확인 -> 있으면 추가로 이름 붙여서 저장
            fname, ext = os.path.splitext(str(uploadedFile))
            uuidfilename = str(uuid.uuid1()).replace('-', '')
            try:
                s3.upload_fileobj(uploadedFile, AWS_STORAGE_BUCKET_NAME, user_id + "/" + file_path + uuidfilename + ext)
            except:
                # 실패 시
                return JsonResponse({
                    'result': 'Upload failed',
                })
    # 파일 업로드 성공
    return JsonResponse({
        'result': 'Upload succeed',
    }, status=201)


@csrf_exempt
def listFile(request):
    if request.method == 'GET':
        file_path = request.GET["file_path"]
        user_id = request.GET["user"]

        file_path_list = file_path.split("/")
        file_path_list.insert(0, user_id)

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
                    file = content['Key']
                    full_file_split = file.split("/")
                    for item in file_path_list:
                        if item in full_file_split:
                            full_file_split.remove(item)
                    file_split = full_file_split
                    print(file_split)
                    if file[-1] == "/":
                        folder_list.append(file_split[0])
                    else:
                        if (len(file_split)) == 1:
                            file_list.append(file_split[0])

        except:
            return JsonResponse({
                'result': 'Path Error',
            })

        print("file_list", file_list)
        print("folder_list", folder_list)
        response = {
            'folders': folder_list,
            'files': file_list,
        }
        return JsonResponse(response)


@csrf_exempt
def listImageFile(request):
    if request.method == "GET":
        user_id = request.GET['user_id']  # user별 폴더
        paginator = s3.get_paginator('list_objects_v2')
        image_file_url = []
        try:
            response_iterator = paginator.paginate(
                Bucket=AWS_STORAGE_BUCKET_NAME,
                Prefix=user_id
            )
            for page in response_iterator:
                for content in page['Contents']:
                    file = content['Key']
                    if '.jpg' in file or '.png' in file:
                        file_url = 'https://{0}.s3.{1}.amazonaws.com/{2}'.format(AWS_STORAGE_BUCKET_NAME, AWS_REGION,
                                                                                 file)
                        image_file_url.append(file_url)

            response = {
                'image_files': image_file_url,
            }
            return JsonResponse(response)
        except:
            return JsonResponse({
                'result': 'No such user'
            })


@csrf_exempt
def downloadFile(request):
    # file_path = request.GET['file_path']
    file_name = request.GET['file_name']  # 파일 이름
    user_id = request.GET['user_id']
    try:
        paginator = s3.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Prefix=user_id
        )
    except:
        return JsonResponse({
            'result': 'No such user'
        })
    file_url = ""
    for page in response_iterator:
        for content in page['Contents']:
            key = content['Key']
            key_name = key.split("/")[-1]
            print(key_name)
            print(file_name)
            if key_name == file_name:
                file_url = 'https://{0}.s3.{1}.amazonaws.com/{2}'.format(AWS_STORAGE_BUCKET_NAME, AWS_REGION,
                                                                         key)
                '''s3.generate_presigned_url('get_object',
                                       Params={'Bucket': AWS_STORAGE_BUCKET_NAME,
                                               'Key': object_name},
                                       ExpiresIn=expiration)'''

    if file_url == "":
        return JsonResponse({
            'result': 'Failed'
        })
    else:
        response = {
            'file': file_url,
        }
        return JsonResponse(response)

    # 오브젝트 이름 -> 다운 받을 이름
    # file_path = 다운 경로
    # print(s3.download_file(AWS_STORAGE_BUCKET_NAME, down_path, file_name))
    # return s3.download_file(AWS_STORAGE_BUCKET_NAME, down_path, file_name)
#    return S3.download_file(bucket, user+"/"+key, local_path)
