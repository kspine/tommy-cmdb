from django.shortcuts import render,redirect,HttpResponse
from .form import *
from cmdb.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tommy_cmdb.settings import *
import os,datetime,json
from .command import *
# Create your views here.

def jifang_add(request):
    """添加机房"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员
    jifang_list=Jifang.objects.all()#获取所有信息
    paginator = Paginator(jifang_list, 10)#每列10条
    page = request.GET.get('page')  # 获取用户输入的页数
    try:
        contacts = paginator.page(page)  # 获取用户输入的页来获取当页数据
    except PageNotAnInteger:
        page = 1
        contacts = paginator.page(1)  # 如果没有输入，默认第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 用户输入错误返回

    if request.method=="GET":
        obj = Jifang_Add_Form()
        return render(request,"assets/jifang_add.html",locals())
    elif request.method == "POST":
        obj=Jifang_Add_Form(request.POST)
        if obj.is_valid():
            jifang_name=obj.cleaned_data["jifang_name"]
            is_cunzai = Jifang.objects.filter(jifang_dizhi=jifang_name)
            #print(is_cunzai)
            if not is_cunzai:
                Jifang.objects.create(jifang_dizhi=jifang_name,create_time=datetime.datetime.now())
                user = Users.objects.get(username=request.session.get("username"))
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(user.username) + "执行添加机房" + str(jifang_name) + "成功")
                return redirect("assets/jifang_add")
            else:
                add_jifang_err="机房名字存在"
                user = Users.objects.get(username=request.session.get("username"))
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(user.username) + "执行添加机房" + str(jifang_name) + "失败，机房存在")
            return render(request, "assets/jifang_add.html", locals())
        else:
            return render(request,"assets/jifang_add.html",locals())

def jifang_del(request):
    """删除机房"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
    req_status=""
    print(request.META['HTTP_REFERER'])
    if request.method=="POST":
        jifang_id=request.POST.get("del_id",None)
        if jifang_id:
            user = Users.objects.get(username=request.session.get("username"))
            Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                  histry_txt=str(user.username) + "执行删除机房" + str(Jifang.objects.get(pk=jifang_id).jifang_dizhi) + "成功")
            Jifang.objects.get(pk=jifang_id).delete()
            req_status = "1"
        else:
            req_status = "参数错误，联系管理员"
    else:
        req_status="未知错误，联系管理员"
    return HttpResponse(json.dumps({"req_status":req_status}),content_type="application/json")

def host_add(request):
    """添加主机"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
    xinxi=""
    jifang_list = Jifang.objects.all()
    user_group_list = User_Groups.objects.all()
    if request.method=="GET":
        obj=Host_Add_Form()
        return render(request,"assets/host_add.html",locals())
    elif request.method=="POST":
        obj=Host_Add_Form(request.POST)
        if obj.is_valid():
            host_ip=obj.cleaned_data["ip"]
            host_obj=Hosts.objects.filter(ip=host_ip)
            if not host_obj:
                host_port=obj.cleaned_data["port"]
                host_user = obj.cleaned_data["user"]
                host_password = obj.cleaned_data["password"]
                host_jifang = Jifang.objects.get(pk=int(request.POST.get("jifang")))
                host_user_groups=User_Groups.objects.filter(pk__in=request.POST.getlist("user_group"))
                host_status = request.POST.get("host_status")
                create_time = datetime.datetime.now()
                host_obj=Hosts()
                host_obj.ip=host_ip
                host_obj.port=host_port
                host_obj.password=host_password
                host_obj.jifang=host_jifang
                host_obj.user=host_user
                host_obj.status=host_status
                host_obj.create_time=create_time
                host_obj.save()
                host_obj=Hosts.objects.get(ip=host_ip)
                if host_user_groups:
                    for host_user_group in host_user_groups:
                        host_obj.user_groups.add(host_user_group)
                    host_obj.save()
                xinxi="添加成功"
                user = Users.objects.get(username=request.session.get("username"))
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(user.username) + "执行添加主机" + str(host_ip) + "成功")

            else :
                xinxi="主机存在，不能重复添加"

            #print(request.POST.getlist("user_group"))
            #Hosts.objects.create(ip=host_ip,port=host_port,user=host_user,password=host_password,status=host_status,create_time=create_time,user_groups=host_user_groups,jifang=host_jifang)
            return render(request, "assets/host_add.html", locals())
        else:
            return render(request, "assets/host_add.html", locals())

def host_list(request):
    if not request.session.get("is_active", None):
        return redirect("/login/")
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员
    login_user_group = User_Groups.objects.get(users__username=request.session.get("username"))
    #print(login_user_group)
    host_lists = Hosts.objects.all().filter(user_groups=login_user_group)#返回普通用户组所有主机
    #print(host_lists)
    if login_user_is_super == '1':#如果是管理员组，返回所有数据
        host_lists = Hosts.objects.all()
    paginator = Paginator(host_lists, 10)  # 每列10条
    page = request.GET.get('page')  # 获取用户输入的页数
    try:
        contacts = paginator.page(page)  # 获取用户输入的页来获取当页数据
    except PageNotAnInteger:
        page = 1
        contacts = paginator.page(1)  # 如果没有输入，默认第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 用户输入错误返回

    #print(Hosts.objects.get(pk=7).jifang)
    if request.method=="GET":
        return render(request,"assets/host_list.html",locals())

def host_edit(request,edit_host_id):
    """修改主机"""
    if not request.session.get("is_active", None):
        return redirect("/login/")
        ###判断用户是否管理员###
    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员
    if login_user_is_super == "0":
        req_status = "没有权限"
        return render(request, "assets/host_edit.html", locals())
    user_group_obj=User_Groups.objects.all()
    #print (Hosts.objects.get(pk=edit_host_id).user_groups.values_list("id"))#通过主机ID获取group iD
    host_user_groups=Hosts.objects.get(pk=edit_host_id).user_groups.values_list("id")
    host_user_groups_id=[]
    for value in host_user_groups:
        #print(i[0])
        #print(value[0])
        host_user_groups_id.append(value[0])
    print(host_user_groups_id)
    req_status=""
    if request.method=="GET":
        edit_host_obj=Hosts.objects.get(pk=int(edit_host_id))
        jifang_obj = Jifang.objects.all()

        return render(request,"assets/host_edit.html",locals())
    if request.method=="POST":
        #print(request.path_info)
        port=request.POST.get("port")
        user = request.POST.get("username")
        status = request.POST.get("status")
        password = request.POST.get("password")
        jifang = Jifang.objects.get(pk=request.POST.get("jifang"))
        host_user_groups = User_Groups.objects.filter(pk__in=request.POST.getlist("user_group"))
        host_obj = Hosts.objects.get(pk=edit_host_id)
        host_obj.port=port
        host_obj.user=user
        host_obj.password=password
        host_obj.status=status
        host_obj.jifang=jifang
        host_obj.save()
        host_obj = Hosts.objects.get(pk=edit_host_id)
        #删除原来的组
        for i in host_user_groups_id:
            host_obj.user_groups.remove(User_Groups.objects.get(id=i))
        #添加新的用户组
        if host_user_groups:
            for host_user_group in host_user_groups:
                host_obj.user_groups.add(host_user_group)
            host_obj.save()

        req_status = "修改成功"
        user = Users.objects.get(username=request.session.get("username"))
        Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                              histry_txt=str(user.username) + "执行修改主机" + str(host_obj.ip) + "成功")
        return redirect("/assets/host_list/")
    else:
        req_status="未知错误，联系管理员"
    return HttpResponse(json.dumps({"req_status":req_status}),content_type="application/json")

def host_del(request):
    #######删除主机##############
    if not request.session.get("is_active", None):
        return redirect("/login/")
    if request.method=="GET":
        req_status = "没有权限"
        return HttpResponse(json.dumps({"req_status": req_status}), content_type="application/json")
    elif request.method=="POST":
        id = request.POST.get("id")
        ##删除host和user组关联
        host_user_groups = Hosts.objects.get(pk=id).user_groups.values_list("id")
        host_user_groups_id = []
        host_obj=Hosts.objects.get(pk=id)
        for value in host_user_groups:
            host_obj.user_groups.remove(User_Groups.objects.get(id=value[0]))
            host_obj.save()
        user = Users.objects.get(username=request.session.get("username"))
        Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                              histry_txt=str(user.username) + "执行删除主机" + str(host_obj.ip) + "成功")
        host_obj.delete()
        #Hosts.objects.get(pk=id).delete()
        req_status = "1"
        return HttpResponse(json.dumps({"req_status": req_status}), content_type="application/json")

def host_shell(request):
    """执行shell"""
    if not request.session.get("is_active", None):
        return redirect("/login/")

    if request.method=="POST":
        ip = request.POST.get("ip",None)
        port = request.POST.get("port", None)
        user = request.POST.get("user", None)
        password = request.POST.get("password", None)
        cmd = request.POST.get("cmd", None)
        if ip or port or user or password or cmd:
            print(ip,port,user,password,cmd)
            ret = command(ip=ip,port=port,user=user,password=password,cmd=cmd)
            user = Users.objects.get(username=request.session.get("username"))
            req_status=0
            if ret==0:
                print("连接错误")
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(ip) + "执行" + str(cmd) + "失败")
                return HttpResponse(json.dumps({"req_status": req_status}), content_type="application/json")

            else:
                req_status=1
                Histry.objects.create(user=user, create_date=datetime.datetime.now(),
                                      histry_txt=str(ip) + "执行" + str(cmd) + "成功")
                return HttpResponse(json.dumps({"req_status": req_status}), content_type="application/json")

                print(ret.readlines())
    else:
        pass

def history(request):
    """日志"""
    if not request.session.get("is_active", None):
        return redirect("/login/")

    user_obj = Users.objects.get(username=request.session.get("username"))
    login_user_is_super = user_obj.user_groups.is_super  # 0普通用户,1管理员
    #login_user_group = User_Groups.objects.get(users__username=request.session.get("username"))
    # print(login_user_group)
    history_lists = Histry.objects.all().filter(user=Users.objects.filter(username=request.session.get("username"))).order_by("-id")
    #host_lists = Hosts.objects.all().filter(user_groups=login_user_group)  # 返回普通用户组所有主机
    # print(host_lists)
    if login_user_is_super == '1':  # 如果是管理员组，返回所有数据
        history_lists = Histry.objects.all().order_by("-id")
    paginator = Paginator(history_lists, 10)  # 每列10条
    page = request.GET.get('page')  # 获取用户输入的页数
    try:
        contacts = paginator.page(page)  # 获取用户输入的页来获取当页数据
    except PageNotAnInteger:
        page = 1
        contacts = paginator.page(1)  # 如果没有输入，默认第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 用户输入错误返回



    return render(request,"assets/history.html",locals())

def host_info(request,host_id):
    """主机信息"""
    if not request.session.get("is_active", None):
        return redirect("/login/")

    if request.method=="GET":
        host_obj=Hosts.objects.get(pk=host_id)
        ####os###
        os = command(ip=host_obj.ip,port=host_obj.port,user=host_obj.user,password=host_obj.password,cmd="cat /etc/redhat-release").readlines()[0]
        print(os)
        ###负载###
        uptime = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1").readlines()[0]).strip()
        if "days" in uptime:
            load_1 = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1|awk -F [,:] '{print $8}'").readlines()[0]).strip()
            load_5 = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1|awk -F [,:] '{print $9}'").readlines()[0]).strip()
            load_15 = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1|awk -F [,:] '{print $10}'").readlines()[0]).strip()
        else:
            load_1 = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1|awk -F [,:] '{print $7}'").readlines()[0]).strip()
            load_5 = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1|awk -F [,:] '{print $8}'").readlines()[0]).strip()
            load_15 = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="w|head -1|awk -F [,:] '{print $9}'").readlines()[0]).strip()
        print(load_1,load_5,load_15)
        ###mem###
        mem_total=str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="free -m|grep Mem:|awk '{print $2}'").readlines()[0]).strip()#总内存
        mem_free = str(command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="free -m|grep Mem:|awk '{print $4}'").readlines()[0]).strip()#剩余内存
        mem_shiyonglv=100-int(float(mem_free)*100//float(mem_total))
        print(mem_shiyonglv)
        print("剩余内存:"+mem_free,"总内存:"+mem_total,"内存剩余率:"+str(float(mem_free)*100//float(mem_total))+"%")
        ###disk###
        disk =command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="df -h |sed -n '2,$p'").readlines()
        for index,i in enumerate(disk):
            #print(str(i).replace('\n',''))
            disk[index]=str(i).replace('\n','')
        print(disk)

        #df -h |sed -n '2,$p'|awk '{print $5,$6}'
        disk1=command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="df -h |sed -n '2,$p'|awk '{print $5,$6}'").readlines()
        for index,i in enumerate(disk1):
            #print(str(i).replace('\n',''))
            mount_dir=str(i).split(" ")[0].replace("%","")
            shiyonglv=str(i).split(" ")[1].replace("\n","")
            disk1[index]=(mount_dir,shiyonglv)
        print(disk1)
        ###监听端口####
        listen = command(ip=host_obj.ip, port=host_obj.port, user=host_obj.user, password=host_obj.password,cmd="netstat -tlunp|sed -n '3,$p'").readlines()
        for index,i in enumerate(listen):
            #print(str(i).replace('\n',''))
            listen[index]=str(i).replace('\n','')
        print(listen)

        return  render(request,"assets/host_info.html",locals())

def command_ip(request):
    if not request.session.get("is_active", None):
        return redirect("/login/")

    if request.method=="GET":
        req=command("192.168.80.201", 22, "root", "123456", "ifconfig")
        req=req.readlines()
        for index,value in enumerate(req):
            req[index]=str(value).replace("\n","")
        print(req)
        return render(request,"assets/command.html",locals())



def text(request):
    group=User_Groups.objects.get(pk=10)
    print(group.hosts_set.values,type(group.hosts_set.values))
    for i in group.hosts_set.values_list():
        print(i)