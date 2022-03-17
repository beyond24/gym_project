"""gym_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.views import index, acount, count, article, coach, course

urlpatterns = [
    path('', course.course_list,name='home'),

    # 后台的控制台count
    path('dashboard/', count.dashboard, name='dashboard'),

    # 启用media
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    path('admin/', admin.site.urls),

    # acount
    path('index/', index.index),
    path('login/', acount.login, name='login'),
    path('register/', acount.register),
    path('image/code/', acount.image_code),
    path('logout/', acount.logout),

    # article
    path('article/list/', article.article_list, name='article_list'),
    path('article-detail/<int:nid>/', article.article_detail, name='article_detail'),
    # 发表评论
    path('post-comment/<int:article_id>/', article.post_comment, name='post_comment'),


    # coach
    path('coach/list/', coach.coach_list),

    # course
    path('course/list/', course.course_list),
    path('course-detail/<int:nid>/', course.course_detail, name='course_detail'),
    path('course/buy/', course.buy_course),
    path('mycourse/<int:nid>/', acount.my_course),


]
