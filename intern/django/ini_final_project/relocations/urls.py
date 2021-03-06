from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main, name='main'),
    path('video_list', views.video_list, name='video_list'),
    path('video_manage', views.video_information, name='video_manage'),
    path('watching/<int:vid>', views.video_count, name='counts'),
    path('join', views.signup, name='join'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('upload', views.upload_file, name='upload'),
    path('video_manage/<int:vid>', views.delete_video, name='delete_video'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)