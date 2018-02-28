from django import forms

#class user_add(forms.Form):
#    username = forms.CharField(max_length=20, label="用户名", widget=forms.TextInput(attrs={'size': '35'}))
#    password = forms.CharField(max_length=30, label="密  码", widget=forms.PasswordInput(attrs={'size': '35'}))

class User_Group_Form(forms.Form):
    group_name = forms.CharField(max_length=20,label="组名")

class User_Add_Form(forms.Form):
    username = forms.CharField(max_length=20, label="用户名")
    password = forms.CharField(max_length=20, label="密码", widget=forms.PasswordInput)
