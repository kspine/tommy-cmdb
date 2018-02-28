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
    url(r'jifang_add', jifang_add,name="jifang_add"),#机房
    url(r'jifang_del', jifang_del,name="jifang_del"),#机房删除
    url(r'host_add', host_add,name="host_add"),#主机添加
    url(r'host_list', host_list,name="host_list"),#主机列表
    url(r'host_edit/(\d+)', host_edit,name="host_edit"),#主机添加
    url(r'host_del/', host_del,name="host_del"),#主机删除
    url(r'command_ip', command_ip, name="command_ip"),  # 主机列表
    url(r'host_shell/',host_shell,name="host_shell"), #执行shell命令
    url(r'history/',history,name="history"), #执行shell命令
    url(r'host_info/(\d+)',host_info,name="host_info"), #主机当前信息
    url(r'text',text,name="text")




]
