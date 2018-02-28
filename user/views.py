from django.shortcuts import render,redirect,HttpResponse
from .form import *
from cmdb.models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from tommy_cmdb.settings import *
import os,datetime,json
# Create your views here.
def user_add(request):
    """添加用户"""
    if not request.session.get("is_active",None):
        return redirect("/login/")
    ###判断用户是否管理员###
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员

    user_group_obj=User_Groups.objects.all()
    xinxi=""
    if request.method == "GET":
        obj = User_Add_Form()
        return render(request,"user/user_add.html",locals())
    elif request.method=="POST":
        obj = User_Add_Form(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data["username"]
            password = obj.cleaned_data["password"]
            status = request.POST.get("status")
            groups = User_Groups.objects.get(pk=request.POST.get("groups"))
            create_time=datetime.datetime.now()
            if not Users.objects.filter(username=username):
                Users.objects.create(username=username,password=password,status=status,user_groups=groups,create_time=create_time)
                xinxi="添加成功"
                user=Users.objects.get(username=request.session.get("username"))
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(user.username) + "执行添加用户" + str(username) + "成功")
            else:
                xinxi="用户存在"
                user = Users.objects.get(username=request.session.get("username"))
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(user.username) + "执行添加用户" + str(username) + "失败，用户存在")
            return render(request, "user/user_add.html", locals())
        else:
            return render(request, "user/user_add.html", locals())

def user_list(request):
    if not request.session.get("is_active",None):
        return redirect("/login/")
        ###判断用户是否管理员###
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员

    user_list_obj=Users.objects.all()
    paginator = Paginator(user_list_obj, 10)  # 每列10条
    page = request.GET.get('page')  # 获取用户输入的页数
    try:
        contacts = paginator.page(page)  # 获取用户输入的页来获取当页数据
    except PageNotAnInteger:
        page = 1
        contacts = paginator.page(1)  # 如果没有输入，默认第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 用户输入错误返回

    if request.method == "GET":
        return render(request,"user/user_list.html",locals())

def user_del(request):
    """删除用户"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
    req_status=""
    #print(request.META['HTTP_REFERER'])
    if request.method=="POST":
        user_group_id=request.POST.get("del_id",None)
        if user_group_id:
            user = Users.objects.get(username=request.session.get("username"))
            Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                  histry_txt=str(user.username) + "执行删除用户组" + str(
                                      Users.objects.get(pk=user_group_id).username) + "成功")

            Users.objects.get(pk=user_group_id).delete()
            req_status = "1"
        else:
            req_status = "参数错误，联系管理员"
    else:
        req_status="未知错误，联系管理员"
    return HttpResponse(json.dumps({"req_status":req_status}),content_type="application/json")

def user_edit(request,edit_user_id):
    """修改用户"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
        ###判断用户是否管理员###
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员
    if login_user_is_super == "0":
        req_status = "没有权限"
        return render(request, "user/user_edit.html", locals())
    user_group_obj=User_Groups.objects.all()

    req_status=""
    if request.method=="GET":
        edit_user_obj=Users.objects.get(pk=int(edit_user_id))
        return render(request,"user/user_edit.html",locals())
    if request.method=="POST":
        #print(request.path_info)
        password=request.POST.get("password",None)
        status = request.POST.get("status")
        edit_user_group = User_Groups.objects.get(pk=request.POST.get("groups"))
        user_obj = Users.objects.get(pk=edit_user_id)
        user_obj.password=password
        user_obj.status=status
        user_obj.user_groups=edit_user_group
        user_obj.save()
        req_status = "修改成功"
        user = Users.objects.get(username=request.session.get("username"))
        Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                              histry_txt=str(user.username) + "执行修改用户" + str(user_obj.username) + "成功")
        return redirect("/user/user_list/")
    else:
        req_status="未知错误，联系管理员"
    return HttpResponse(json.dumps({"req_status":req_status}),content_type="application/json")

def user_group(request):
    if not request.session.get("is_active",None):
            return redirect("/login/")
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员

    user_group_obj=User_Groups.objects.all()
    paginator = Paginator(user_group_obj, 10)  # 每列10条
    page = request.GET.get('page')  # 获取用户输入的页数
    try:
        contacts = paginator.page(page)  # 获取用户输入的页来获取当页数据
    except PageNotAnInteger:
        page = 1
        contacts = paginator.page(1)  # 如果没有输入，默认第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 用户输入错误返回



    if request.method == "GET":
        obj=User_Group_Form()
        return render(request,"user/user_group.html",locals())
    if request.method == "POST":
        obj = User_Group_Form(request.POST)
        if obj.is_valid():
            group_name=obj.cleaned_data["group_name"]
            is_super = request.POST.get("is_super")
            create_time = datetime.datetime.now()
            group_obj = User_Groups.objects.filter(group_name=group_name)
            if not group_obj:
                User_Groups.objects.create(group_name=group_name,is_super=is_super,create_time=create_time)
                return redirect("user/user_group/")
            else:
                add_group_err = "用户组存在"
            return render(request, "user/user_group.html", locals())
        else:
            return render(request, "user/user_group.html", locals())


def user_group_del(request):
    """删除用户组"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
    req_status=""
    #print(request.META['HTTP_REFERER'])
    if request.method=="POST":
        user_group_id=request.POST.get("del_id",None)
        if user_group_id:
            user = Users.objects.get(username=request.session.get("username"))
            Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                  histry_txt=str(user.username) + "执行删除用户组" + str(User_Groups.objects.get(pk=user_group_id).group_name) + "成功")
            User_Groups.objects.get(pk=user_group_id).delete()
            req_status = "1"

        else:
            req_status = "参数错误，联系管理员"
    else:
        req_status="未知错误，联系管理员"
    return HttpResponse(json.dumps({"req_status":req_status}),content_type="application/json")
    User_Groups.objects.get(pk=user_group_id).hosts_set

