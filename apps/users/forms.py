
from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile


class RegisterForm(forms.Form):
    #验证码
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":'验证码错误'})

class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=5)
    password = forms.CharField(required=True,min_length=5)


class ForgetForm(forms.Form):
    #忘记密码
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":'验证码错误'})


class ModifyPwdForm(forms.Form):
    #验证码
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birday','gender','mobile','address']