from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


urlpatterns = [
    path("upload/", views.uploadFile, name="uploadFile"),
    path("download/", views.downloadFile, name="downloadFile"),
    path("", views.listFile, name="listFile"),
    path("image/", views.listImageFile, name="listImageFile"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
