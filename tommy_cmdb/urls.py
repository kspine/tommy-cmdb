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
from django.conf.urls import url,include
from django.contrib import admin
from cmdb.views import *
from .settings import *
from django.views.static import *
urlpatterns = [
    url(r'^login/', login,name="login"),#登录
    url(r'^loginout/', loginout,name="loginout"),#注销
    url(r'^admin/', admin.site.urls),
    url(r'^$', index,name="index"),#首页
    url(r'^user/', include('user.urls')),#用户管理模块
    url(r'^assets/', include('assets.urls')),#资产管理模块

    url(r'^gropus/', groups,name="groups"),#组管理
    url(r'^zhuce/', zhuce, name="zhuce"),  # 组管理
    url(r'^upload/$', upload, name="upload"),  # 组管理
url(r'^upload_db/$', upload_db, name="upload_db"),  # 组管理
url(r"^upload/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT,}),
    url(r'^webssh/', webssh, name="webssh"),  # 组管理


]
