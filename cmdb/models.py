from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=20,verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    status = models.CharField(max_length=1,choices=(('0','禁用'),('1','启用')),default='1',verbose_name="用户状态")
    user_groups = models.ForeignKey("User_Groups",verbose_name="用户所属组",null=True,blank=True,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural="用户信息"
    def __str__(self):
        return self.username

class User_Groups(models.Model):
    group_name = models.CharField(max_length=20, verbose_name="组名")
    status = models.CharField(max_length=1, choices=(('0', '禁用'), ('1', '启用')), default='1', verbose_name="组状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_super = models.CharField(max_length=1, choices=(('0', '普通用户组'), ('1', '管理组')), default='0', verbose_name="是否管理组")
    class Meta:
        verbose_name = "用户组信息"
        verbose_name_plural = "用户组信息"
    def __str__(self):
        return self.group_name
class Hosts(models.Model):
    ip = models.CharField(max_length=20, verbose_name="ip")
    password = models.CharField(max_length=30, verbose_name="密码")
    port = models.CharField(max_length=5,default='22', verbose_name="端口")
    user = models.CharField(max_length=15, verbose_name="用户")
    status = models.CharField(max_length=1, choices=(('0', '禁用'), ('1', '启用')), default='1', verbose_name="组状态")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    user_groups = models.ManyToManyField("User_Groups",verbose_name="所属组",null=True,blank=True)
    jifang = models.ForeignKey("Jifang", verbose_name="所属机房",null=True,blank=True,on_delete=models.SET_NULL)
    class Meta:
        verbose_name = "主机信息"
        verbose_name_plural = "主机信息"
    def __str__(self):
        return self.ip
class Host_info(models.Model):
    os = models.TextField( verbose_name="os")
    cpu = models.TextField( verbose_name="cpu")
    disk = models.TextField( verbose_name="disk")
    mem = models.TextField( verbose_name="mem")
    network = models.TextField( verbose_name="network")
    Hosts = models.ForeignKey(Hosts)
    class Meta:
        verbose_name = "主机详细信息"
        verbose_name_plural = "主机详细信息"
    def __str__(self):
        return self.Hosts.ip


class Jifang(models.Model):
    jifang_dizhi=models.CharField(max_length=20, verbose_name="机房")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    class Meta:
        verbose_name = "机房信息"
        verbose_name_plural = "机房信息"
    def __str__(self):
        return self.jifang_dizhi
class Histry(models.Model):
    create_date=models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    histry_txt = models.CharField(max_length=100, verbose_name="执行说明")
    user = models.ForeignKey("Users",verbose_name="用户",null=True,blank=True,on_delete=models.SET_NULL)
    class Meta:
        verbose_name = "历史信息"
        verbose_name_plural = "历史信息"
    def __str__(self):
        return self.histry_txt

class Upload_db(models.Model):
    username = models.CharField(max_length=10,verbose_name="用户名")
    file = models.FileField(upload_to="./upload/%Y/%m/%d")
