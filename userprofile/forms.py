# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile


# 登录表单，继承了forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio',)


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16)
    password2 = forms.CharField(max_length=16)

    class Meta:
        model = User
        fields = ('username', 'email')

    def check_password(self):
        data = self.cleaned_data
        if data['password1'] == data['password2']:
            return data['password1']
        else:
            raise forms.ValidationError("密码不一致，请重新输入！")
