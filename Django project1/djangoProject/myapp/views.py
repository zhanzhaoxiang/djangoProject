import os
import random
from io import BytesIO

from PIL import ImageDraw, ImageFont, ImageFilter, Image
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .models import *


# Create your views here.


def register(request):
    if request.method == 'POST':
        # 获得表单值
        user_register_form = UserRegisterForm(request.POST)
        # 验证
        flag = user_register_form.is_valid()
        if flag:
            # 将数据接收形成一个字典
            data = user_register_form.cleaned_data
            password = make_password(data['password'])
            user = User.objects.create(username=data['username'], password=password, phone=data['phone'],
                                       email=data['email'], country=data['country'], usertype_id=1)
            if user:
                return redirect(reverse('myapp:login'))
        return render(request, 'register.html',locals())

    else:
        user_register_form = UserRegisterForm()
        return render(request, "register.html", locals())

def login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)

        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            username = data['username']
            password = data['password']
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['username'] = username
                return HttpResponse('登录成功')
        else:
            print('不成功')
    user_login_form = UserLoginForm()
    return render(request, 'login.html', locals())


# 用验证码插件验证
def valid(request):
    key = request.GET.get('key')
    code = request.GET.get('code')

    captcha_obj = CaptchaStore.objects.get(hashkey=key)
    if captcha_obj.response == code.lower():
        data = {'msg':'验证通过'}
    else:
        data = {'msg':'验证失败'}
    return JsonResponse(data)


# 自定义生成验证码
def get_color():
    red = random.randint(0,256)
    green = random.randint(0, 256)
    blue = random.randint(0, 256)
    return red, green, blue


def get_code():
    s='0123456789qwertyuiopasdfghjklzxcvbnmZMXNCBVLASKDJFHGQPOWIERUYT'
    code = ''
    for i in range(4):
        code += random.choice(s)
    return code


def draw(request):
    # 指定画布长宽
    width = 120
    height = 40
    image_size = (width,height)
    # 定义画布
    image = Image.new('RGB', image_size, get_color())
    # 定义画笔
    draw = ImageDraw.Draw(image)
    # 绘制干扰线
    for i in range(10):
        # 指定起始结束位置
        begin = (random.randint(0,width), random.randint(0,height))
        end = (random.randint(0, width), random.randint(0, height))
        # 使用画笔绘制，并定义样式颜色等
        draw.line((begin,end), fill=(get_color()))
    # 绘制干扰点
    for i in range(20):
        draw.point((random.randint(0,width), random.randint(0,height)),fill=(get_color()))
    # 产生验证码
    code = get_code()
    # 指定字体和大小
    myfont = ImageFont.truetype(font='static/fonts/arial.ttf', size=30)
    # 逐个绘制字符
    for i in range(4):
        # 每绘制一个，x周位置改变，y可以不变
        distance_x = random.randint(30*i,30*i+5)
        distance_y = random.randint(0,5)
        draw.text((distance_x,distance_y),code[i],font=myfont,fill=(get_color()))

    # 滤镜边界加强
    image= image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # 定义一个缓存
    buffer = BytesIO()
    # 将图片放到缓存
    image.save(buffer,'JPEG')
    # 获取缓存内容
    buf_bytes = buffer.getvalue()
    # 将code保存到session中用于验证
    request.session['code'] = code
    return HttpResponse(buf_bytes,'image/jpeg')


def login1(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        real_code = request.session['code']
        user_login_form = UserLoginForm(request.POST)
        if code.lower()==real_code.lower():

            if user_login_form.is_valid():
                data = user_login_form.cleaned_data
                username = data['username']
                password = data['password']
                try:
                    user = User.objects.get(username=username)
                    if check_password(password, user.password):
                        request.session['username'] = username
                        return HttpResponse('登录成功')
                    else:
                        return render(request, 'login1.html', {'msg': '用户名或密码有误','user_login_form':user_login_form})
                except:
                    return render(request,'login1.html',{'msg':'无用户','user_login_form':user_login_form})

            else:
                return render(request, 'login1.html', {'msg': '用户名或密码有误','user_login_form':user_login_form})
        else:
            return render(request,'login1.html',{'msg':'验证码错误','user_login_form':user_login_form})
    user_login_form = UserLoginForm()
    return render(request, 'login1.html',locals())