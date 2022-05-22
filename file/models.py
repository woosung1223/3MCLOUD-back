from django.db import models
# from django.contrib.auth.models import AbstractUser


class Folder(models.Model):
    folder_id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=200)
    parent_folder = models.ForeignKey("self", related_name="child_folder", on_delete=models.CASCADE, null=True, default='')
#    user_id = models.ForeignKey(AbstractUser, related_name="folder_user", on_delete=models.CASCADE)


class File(models.Model):
    file_name = models.CharField(max_length=200, null=True) # 파일 이름 models.CharField()
    parent = models.ForeignKey(Folder, related_name="child_file", on_delete=models.CASCADE, default=123)
    user_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜
    extension = models.CharField(max_length=20)
    uuid_file_name = models.CharField(max_length=32)
    #user_id = models.ForeignKey(AbstractUser, related_name="file_user", on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.id}: {self.file_name}'


