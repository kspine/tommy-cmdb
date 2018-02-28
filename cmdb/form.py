from django import forms

class Login(forms.Form):
    username = forms.CharField(max_length=20,label="用户名",widget=forms.TextInput(attrs={'size': '35'}))
    password = forms.CharField(max_length=30,label="密  码",widget=forms.PasswordInput(attrs={'size': '35'}))

class ZhuChe(forms.Form):
    username = forms.CharField(max_length=20,label="用户名")
    pwd = forms.CharField(max_length=20,min_length=6)
    email = forms.EmailField(label="邮箱")
    ip = forms.GenericIPAddressField(label="IP地址")
class upload_db_test(forms.Form):
    username = forms.CharField(max_length=10,label="用户名")
    file = forms.FileField()
