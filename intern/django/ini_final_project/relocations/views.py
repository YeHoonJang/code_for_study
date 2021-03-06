from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Contents

import pymysql
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(request):
    return render(request, 'relocations/main.html')


class VideoList(generic.ListView):
    template_name = 'relocations/video_list.html'
    context_object_name = 'contents_list'

def video_list(request):
    video_list_dict = Contents.objects.values()
    video_list = []
    for i in video_list_dict:
        if i['status'] != 'deleted':
            video_list.append(i)
    return render(request, 'relocations/video_list.html', {'contents_list':video_list})


def video_information(request):
    video_info_dict = Contents.objects.values()
    video_info_list = []
    for i in video_info_dict:
        if i['author'] == request.user.username and i['status'] != 'deleted':
            video_info_list.append(i)
    return render(request, 'relocations/video_manage.html', {'content_info_list': video_info_list})


#실제 파일 relocate만 하면 돼!

def video_count(request, vid):
    selected_video = Contents.objects.get(pk=vid)
    selected_video.counts += 1
    selected_video.save()

    current_level = get_current_level(vid)
    target_level = check_video_level(selected_video.counts)

    if current_level != target_level[0]:
        selected_video.level = target_level[0]
        selected_video.file = target_level[1]
        selected_video.save()

        conn = connect_mysql()
        curs = conn.cursor()
        sql = "UPDATE relocations_contents SET level='%s', file='%s' WHERE id=%s" % (target_level[0], target_level[1], vid)
        curs.execute(sql)
        conn.commit()

    content_route = str(Contents.objects.get(pk=vid).file).split('/')[-1]
    content_route = os.path.join(str(target_level[1]), content_route)

    content_route_dict = {'content_route':content_route}
    return render(request, 'relocations/watching.html', content_route_dict)

def get_current_level(vid):
    conn = connect_mysql()
    curs = conn.cursor()
    sql = "SELECT level FROM relocations_contents WHERE id=%s" % (vid)
    curs.execute(sql)
    return curs.fetchall()[0][0]

def check_video_level(counts):
    conn = connect_mysql()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute("SELECT * FROM level")
    rows = curs.fetchall()
    for row in rows:
        if row['min_count'] <= counts <= row['max_count']:
            target_level = row['level']
            target_level_path = row['path']
            print(target_level, target_level_path)
            print([target_level, target_level_path])
            return [target_level, target_level_path]


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('main')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm()
    return render(request, 'relocations/adduser.html', {'form': form})


def connect_mysql():
    return pymysql.connect(host='localhost', user='root', password='ini6223', db='django_db', charset='utf8')


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        title = request.POST['title']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        if request.user.is_authenticated:
            author = request.user.username

        #pymysql 로 mysql 에 data insert
        conn = connect_mysql()
        curs = conn.cursor()

        sql = "INSERT INTO relocations_contents VALUES (null, '%s', '%s', '%s', now(), 0, 'uploaded', 'bronze')" % (title, uploaded_file_url, author)

        curs.execute(sql)
        conn.commit()
        curs.close()

        return render(request, 'relocations/upload.html',
                      {'uploaded_file_url':uploaded_file_url})
    return render(request, 'relocations/upload.html')


def delete_video(request, vid):
    deleted_video = Contents.objects.get(pk=vid)
    deleted_video.status = 'deleted'
    deleted_video.save()

    conn = connect_mysql()
    curs = conn.cursor()

    sql = "UPDATE relocations_contents SET upload_date=now() WHERE id=%s" % (vid)
    curs.execute(sql)
    conn.commit()

    return video_information(request)