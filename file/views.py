import uuid
from .models import Folder, File
import os
from django.http import FileResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404, render

AWS_ACCESS_KEY_ID = settings.AWS_S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_S3_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@csrf_exempt
def uploadFile(request, folder_id):
    # 폴더 임시 생성 (테스트용)
    new_folder = Folder(
        folder_id=folder_id,
        user_id=123,
    )
    new_folder.save()

    folder = get_object_or_404(Folder, folder_id=folder_id) # 폴더 데이터 가져옴
    if request.method == "POST":
        # 여러개 파일 저장
        uploadedFiles = request.FILES.getlist('files')
        user_id = "test" #임시 user 생성
        for uploadedFile in uploadedFiles:
            # 예외 처리: 이름 같은 파일 없는지 확인 -> 있으면 추가로 이름 붙여서 저장
            fname, ext = os.path.splitext(str(uploadedFile))
            uuidfilename = str(uuid.uuid1()).replace('-', '')
            # sqlite 저장
            new_file = File(
                file_name=str(uploadedFile),
                uuid_file_name=uuidfilename,
                parent=folder,
                user_id=user_id,
                extension=ext,
            )
            new_file.save()

            try:
                s3.upload_fileobj(uploadedFile, AWS_STORAGE_BUCKET_NAME, user_id + "/" + uuidfilename)
            except:
                # 실패 시 삭제
                File.objects.get(pk=new_file.id).delete()
                return JsonResponse({
                    'result': 'Upload failed',
                })
    # 파일 업로드 성공
    return JsonResponse({
        'result': 'Upload succeed',
    })

def downloadFile(request, file_id):
    file_path = os.path.abspath("media/result/")
    file_name = os.path.basename("media/result/background.png")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="background.png"'

    return response