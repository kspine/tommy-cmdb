from django.shortcuts import render,redirect
from .form import *
from .models import *
from tommy_cmdb.settings import *
import os
# Create your views here.
def index(request):
    """首页"""
    if request.method=="GET":
        if not request.session.get("is_active",None):
            return redirect("/login/")
    user_count=Users.objects.all().count()
    hosts_count=Hosts.objects.all().count()
    user_group_count=User_Groups.objects.all().count()
    jifang_count=Jifang.objects.all().count()
    return render(request,"index.html",locals())

def login(request):
    """用户登录"""
    xinxi=""
    if request.method=="GET":
        if request.session.get("is_active",None):
            return redirect("/")
        else:
            obj = Login()
            return render(request,"login.html",{"obj":obj})
    elif request.method == "POST":
        obj=Login(request.POST)
        if obj.is_valid():
            username=obj.cleaned_data["username"]
            password=obj.cleaned_data["password"]
            user_obj=Users.objects.filter(username=username)
            if user_obj:
                if str(user_obj[0].status)!="1":
                    xinxi = "用户被禁用，请联系系统管理员"
                elif str(password)==str(user_obj[0].password):
                    request.session["is_active"]=True
                    request.session["username"] = username
                    request.session["password"] = password
                    print(user_obj[0].user_groups)
                    request.session["user_groups"] = user_obj[0].user_groups.group_name
                    return redirect("/")
                else:
                    xinxi = "密码错误"
            else:
                xinxi="用户名不存在"
            return render(request,"login.html",{"obj":obj,"xinxi":xinxi})
        else:
            return render(request, "login.html", {"obj": obj})
def loginout(request):
    """用户注销"""
    request.session.flush()
    return redirect("/login/")

def user(request):
    return render(request, "user/user.html")
def groups(request):
    return render(request, "groups/groups.html")

def zhuce(request):
    if request.method=="GET":
        obj = ZhuChe()
        return render(request,"zhuce.html",{"obj":obj})
    else:
        obj = ZhuChe(request.POST)
        if obj.is_valid():
            print(obj)
            return render(request,"zhuce.html",{"obj":obj})
        else:
            print(obj.errors)
            print(obj.errors.as_json())
            return render(request, "zhuce.html", {"obj": obj})

def upload(request):
    if request.method=="GET":
        return render(request,"upload.html")
    elif request.method=="POST":

        obj=request.FILES.get("file")

        try:
            f=open(os.path.join("upload",obj.name),'wb')
        except Exception:
            return render(request, "upload.html", {"data": "请选择文件"})
        for i in obj.chunks():
            f.write(i)
        f.close()
        return render(request,"upload.html",{"data":str(obj.name)+"上传成功"})


def upload_db(request):
    if request.method=="GET":
        obj = upload_db_test()
        return render(request,"upload_db.html",{"obj":obj})
    elif request.method=="POST":
        obj = upload_db_test(request.POST,request.FILES)
        if obj.is_valid():
            username = obj.cleaned_data["username"]
            file = obj.cleaned_data["file"]
            f = Upload_db()
            f.username=username
            f.file=file
            f.save()
            down_url=Upload_db.objects.all().order_by("-id")[0].file
            return render(request,"upload_db.html",{"obj":obj,"xinxi":str(file)+"上传成功","down_url":"http://127.0.0.1:8000/upload/"+str(down_url)})
        else:
            return render(request, "upload_db.html", {"obj": obj, "xinxi": "上传失败"})

def webssh(request):
    return  render(request,"webssh.html")