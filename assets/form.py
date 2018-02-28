from django import forms

class Jifang_Add_Form(forms.Form):
    jifang_name=forms.CharField(max_length=20,label="机房名字",widget=forms.TextInput(attrs={"size":40,}))
class Host_Add_Form(forms.Form):
    ip=forms.GenericIPAddressField(max_length=40,label="IP地址")
    port=forms.IntegerField(label="端口",min_value=1,max_value=65535)
    user=forms.CharField(max_length=20,label="用户名",widget=forms.TextInput)
    password=forms.CharField(max_length=20,label="密码",widget=forms.PasswordInput)