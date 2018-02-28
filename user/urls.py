"""tommy_cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import *

from django.views.static import *
urlpatterns = [
    url(r'^user_add/', user_add,name="user_add"),#登录
    url(r'^user_group/', user_group,name="user_group"),#用户组管理
    url(r'^user_group_del/', user_group_del,name="user_group_del"),#用户组删除
    url(r'^user_list/', user_list,name="user_list"),#用户列表
    url(r'^user_del/',user_del,name='user_del'),#删除用户
    url(r'^user_edit/(\d+)',user_edit,name='user_edit'),#删除用户
]
