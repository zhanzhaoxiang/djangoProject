import re

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm  # 这个包内也有一个forms，但是不对
from .models import *


# 后端构建表单
# 方式1全部自定义
# class UserRegisterForm(Form):
#     username = forms.CharField(max_length=20, min_length=5, error_messages={'min_length': '太短'}, label='用户名：')
#     password = forms.CharField(max_length=10, min_length=5, error_messages={'min_length': '太短', 'max_length': '太长'},
#                                label='密码：', widget=forms.PasswordInput)
#     repassword = forms.CharField(max_length=10, min_length=5, error_messages={'min_length': '太短', 'max_length': '太长'},
#                                  label='确认密码：', widget=forms.PasswordInput)
#     phone = forms.CharField(required=True, error_messages={'required': '手机号必填'}, label='手机号：', widget=forms.NumberInput)
#     email = forms.CharField(required=True, error_messages={'required': '邮箱必填'}, label='邮箱：')
#     country = forms.ChoiceField(required=False, widget=forms.RadioSelect,
#                                 choices=(('中国', '中国'), ('美国', '美国'), ('俄国', '俄国')), label='国家')
#
#     def clean_email(self):
#         """
#         自定义正则验证
#         :return:
#         """
#         email = self.cleaned_data.get('email')
#         flag = re.match(r'[a-zA-Z1-9_]\w{4,}@(\w+)\.\w+$', email)
#         if not flag:
#             raise ValidationError('邮箱有误！')
#         return email


# 方式2 对模型内容添加或减少 ModelForm只能用于创建和编辑，不能由于验证
class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {'password': forms.PasswordInput}
        # 排除字段
        exclude = ['is_super', 'user_type']
        # 加入字段只能自定义


class UserLoginForm(Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={'min_length': '太短'}, label='用户名：')
    password = forms.CharField(max_length=10, min_length=5, error_messages={'min_length': '太短', 'max_length': '太长'},
                               label='密码：', widget=forms.PasswordInput)

    # captcha = CaptchaField(label='验证码')

    # 自定义验证
    def clean_username(self):
        username = self.cleaned_data.get('username')
        flag = re.match(r'[a-zA-Z1-9]\w{5,}$', username)
        if not flag:
            raise ValidationError('用户名格式有误')
        return username
