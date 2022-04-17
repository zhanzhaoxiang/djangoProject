import decimal
import hashlib
import uuid
from alipay import AliPay
from alipay.utils import AliPayConfig

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.core.paginator import *
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.core import serializers

from .models import *
from django.core.cache import cache
from django.conf import settings


# Create your views here.

# 使用cache，装饰器缓存页面
# @cache_page(60 * 5)  # 缓存5分钟
def welcome(request):
    """
    欢迎页面
    :param request:
    :return:
    """
    # 通用方法利用session获取用户名保持登录状态
    # username = request.session.get('username')
    # user = NewUser.objects.filter(username=username).first()
    # return render(request, 'welcome.html', {'user': user})

    # 传入图片
    types = GoodsType.objects.all()
    banners = IndexGoodsBanner.objects.all().order_by("index")
    sales = IndexSaleBanner.objects.all().order_by("index")

    # 分类是标题促销还是广告促销
    for type in types:
        image_adv = IndexGoodsTypeBanner.objects.filter(goodstype=type, display_type=1).order_by('index')
        title_adv = IndexGoodsTypeBanner.objects.filter(goodstype=type, display_type=0).order_by('index')

        # 动态添加属性
        type.image_adv = image_adv
        type.title_adv = title_adv

    # 验证用户登录设置购物车状态
    if request.user.is_authenticated:
        count = Cart.objects.filter(new_user=request.user).count()

    return render(request, 'welcome.html', locals())  # 自动将函数体内的变量打包成字典


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        realname = request.POST.get('realname')
        address = request.POST.get('address')
        age = request.POST.get('age')
        job = request.POST.get('job')
        gender = request.POST.get('gender')
        if username and email and password:
            # 数据库添加
            # 方式1
            # 向user表添加
            user = User()
            user.username = username
            user.phone = phone
            user.password = password
            user.email = email
            # 加密保存16进制
            # user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # user.save()

            # 向级联表添加
            userfile = UserProfile()
            userfile.realname = realname
            userfile.address = address
            userfile.age = age
            userfile.job = job
            userfile.gender = gender
            userfile.user_id = user.id
            # userfile.save()

            # 方式2
            # user = User.objects.create(username=username,phone=phone,password=password)

            # 新方法也注册一个用户
            # 默认密码不加密
            # 对密码进行加密
            password = make_password(password=password)
            new_user = NewUser.objects.create(username=username, email=email, phone=phone, password=password)
            new_user.is_active = 0  # 仅注册未激活状态
            new_user.save()

            # 发送邮件验证激活
            token = str(uuid.uuid4()).replace('-', '')
            # 存储到session中
            request.session['token'] = new_user.id

            path = 'http://127.0.0.1:8000/user_active?token={}'.format(token)

            # 设置邮件主题和内容
            subject = 'fruitoshop邮箱验证'
            message = '''
            欢迎注册fruitoshop，成为我们的会员
            请点击下面的链接激活您的账号！<br>  
            <a href="{}">点击激活</a><br>
            如果链接不可用可以复制到浏览器激活：{} <br>
                            fruitoshop官方团队
            '''.format(path, path)

            from django.conf import settings
            # 如果邮件信息有html标签，需要设置html_message，message只是纯文本，可以有多个接收人,返回接收人的数量
            result = send_mail(subject=subject, message='', from_email=settings.EMAIL_HOST_USER,
                               recipient_list=[email, ], html_message=message)

            return redirect('shop:user_login')
        else:
            # return render(request, 'register.html', {'user': None})
            return render(request, 'register.html')
    # return render(request, 'register.html', {'user': None})
    return render(request, 'register.html')


def user_active(request):
    """
    用户激活
    :param request:
    :return:
    """
    token = request.GET.get('token')
    uid = request.session.get('token')

    new_user = NewUser.objects.get(pk=uid)
    new_user.is_active = 1
    new_user.save()
    return redirect('shop:user_login')


def user_login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 继承AbstractUser类的用户可以有内置登录方法，且密码加密
        # 认证方法authenticate返回一个用户对象
        new_user = authenticate(username=username, password=password)
        if new_user:
            # login直接传入用户对象登录，并且设置session，将new_user保存为user对象，可以直接用request调用
            login(request, new_user)
            response = redirect('shop:welcome')
            if remember == 'on':
                # 设置cookie
                response.set_cookie('username', username)
            return response
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误！'})
    else:
        # 获取cookie
        username = request.COOKIES.get('username')
        return render(request, 'login.html', {'user': username})

        # 普通登录认证方法
        # 取查询集的第一个
    #     user = User.objects.filter(username=username).first()
    #     new_user = NewUser.objects.filter(username=username).first()
    #     if new_user:
    #         # 对已加密的密码验证
    #         # if check_password(password=password, encoded=new_user.password):
    #         # if user.username == username and user.password == password:
    #         #     if user.is_active == 0:
    #         #         return render(request, 'login.html', {'msg': '请先激活'})
    #         #     else:
    #         #         return redirect('shop:detail')
    #         if new_user.username == username and new_user.password == password:
    #             if new_user.is_active == 0:
    #                 return render(request, 'login.html', {'msg': '请先激活'})
    #             else:
    #                 response = redirect('shop:welcome')
    #                 # 存储用户登录状态
    #                 request.session['username'] = new_user.username
    #                 if remember == 'on':
    #                     # 设置cookie，保存用户名，每次登录默认加载这个
    #                     response.set_cookie('username', new_user.username)
    #                     return response
    #                 else:
    #                     return response
    #         else:
    #             return render(request, 'login.html', {'msg': '用户名或密码错误！'})
    #     else:
    #         return render(request, 'login.html', {'msg': '用户不存在！'})
    # else:
    #     username = request.COOKIES.get('username', '')
    #     return render(request, 'login.html', {'username': username, 'user': None})


def user_logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    # 通用退出登录方法
    # request.session.flush()
    # return redirect('shop:welcome')

    # 使用内置退出登录方法
    logout(request)
    return redirect('shop:welcome')


def detail(request):
    """
    用户详情
    :param request:
    :return:
    """
    # 取地址
    addr = Address.objects.filter(new_user_id=request.user.id).first()
    # 取购物车
    count = Cart.objects.filter(new_user=request.user).count()
    # 取订单
    orders = Order.objects.filter(new_user=request.user).order_by('-add_time')
    # 分页显示
    paginator = Paginator(orders, 2)  # 将列表分页，每页两条数据

    for order in orders:
        for status in Order.ORDER_STATUS:
            if order.order_status in status:
                order.status = status[1]
                break
        for pay_method in Order.PAY_METHODS:
            if order.pay_method in pay_method:
                order.paymethod = pay_method[1]
                break

    if request.method == 'POST':
        receive_user = request.POST.get('receive_user')
        receive_address = request.POST.get('receive_address')
        post_code = request.POST.get('post_code')
        phone = request.POST.get('phone')

        addr = Address.objects.create(receive_user=receive_user, receive_address=receive_address, post_code=post_code,
                                      phone=phone, new_user=request.user)
        if addr:
            return redirect('shop:detail')
        else:
            count = Cart.objects.filter(new_user=request.user).count()
            return render(request, 'detail.html', {'msg': '地址添加失败！', 'count': count})

    # 通用方法利用session获取用户名保持登录状态
    # username = request.session.get('username')
    # user = NewUser.objects.filter(username=username).first()
    # return render(request, 'detail.html', {'user': user})

    elif request.method == 'GET':
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

            page = request.GET.get('page')

            try:
                page_obj = paginator.page(page)
            # 页数不是整数返回第一页
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            # 如果页数不存在/不合法，返回最后一页
            except InvalidPage:
                page_obj = paginator.page(paginator.num_pages)

            # page_li = list(page_obj.object_list.values())

            long = ""
            short = ""
            for order in page_obj.object_list:
                short += '<div>' + \
                         '<p class="small" style="float:left;margin-right:2em">订单号:' + str(order.order_id) + '</p>' + \
                         '<p class="small" style="float:left;margin-right:2em">添加时间:' + str(order.add_time) + '</p>' + \
                         '<p class="small">订单状态:' + str(order.status) + '</p>' + \
                         '</div>' + \
                         '<div>' + \
                         '<p class="small" style="float:left;margin-right:2em">收件人:' + str(
                    order.address.receive_user) + '</p>' + \
                         '<p class="small" style="float:left;margin-right:2em">联系电话:' + str(
                    order.address.phone) + '</p>' + \
                         '<p class="small" style="float:left;margin-right:2em">支付方式:' + str(order.paymethod) + '</p>' + \
                         '<p class="small">收货地址:' + str(order.address.receive_address) + '</p>' + \
                         '</div>' + \
                         '<div class="">' + \
                         '<p style="float:left;margin-right:2em">订单商品数量：' + str(order.goods_num) + '</p>' + \
                         '<p style="float:left;color:red">订单总金额：' + str(order.goods_total) + '</p>' + \
                         '<input type="submit" id="pay" class="pay btn btn-success" style=" padding:0;float: right;height: 2em" order_id=' + str(
                    order.order_id) + ' order_status=' + str(order.order_status) + ' pay_method=' + str(
                    order.pay_method) + ' value="去支付">' + \
                         '</div>' + \
                         '<table class="table table-hover" style="border-bottom: 1px solid black">'
                for ordergoods in (OrderGoods.objects.filter(order_id=order.order_id)):
                    short += '<tr>' + \
                             '<td style="width:25%">' + str(ordergoods.goods.name) + '</td>' + \
                             '<td style="width:25%">' + \
                             ' ￥<em>' + str(ordergoods.goods.price) + '</em>/' + str(ordergoods.goods.unite) + '</td>' + \
                             '<td style="width:25%">' + str(ordergoods.number) + '</td>' + \
                             '<td style="width:25%">￥<em>' + str(ordergoods.price) + '</em></td>' + \
                             '</tr>'
                short += '</table>'
            long += short

            result = {
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'num_pages': page_obj.paginator.num_pages,
                'new_page': long
            }
            return JsonResponse(result)

        else:
            for order in orders:
                for status in Order.ORDER_STATUS:
                    if order.order_status in status:
                        order.status = status[1]
                        break
                for pay_method in Order.PAY_METHODS:
                    if order.pay_method in pay_method:
                        order.paymethod = pay_method[1]
                        break

            # 默认第一页
            page_obj = paginator.page(1)
            # page = request.GET.get('page','1')
            # try:
            #     page = int(page)
            # except Exception as err:
            #     page = 1
            #
            # page_obj = paginator.page(page)  # 页码对象
            # # page_obj.object_list得到每页的商品对象

            return render(request, 'detail.html',
                          {'addr': addr, 'count': count, 'orders': orders, 'page_obj': page_obj})


def show(request):
    """
    显示所有用户
    :param request:
    :return:
    """
    # users = User.objects.filter(is_delete=0).all()
    users = User.objects.all()
    return render(request, 'show.html', {'users': users})


def delete(request):
    """
    删除用户
    :param request:
    :return:
    """
    id = request.GET.get('id')
    user = User.objects.get(pk=id)
    if user:

        # # 物理删除,从数据库删除
        # user.delete()

        # 逻辑删除，仅不显示和使用，数据库内还有
        user.is_delete = 1
        user.save()
        return redirect('shop:show')
    else:
        return render(request, 'show.html', {'msg': '删除失败！'})


def delete_goods(request):
    """
    删除商品
    :param request:
    :return:
    """
    id = request.GET.get('id')
    goods = Goods.objects.get(pk=id)
    if goods:

        # # 物理删除,从数据库删除
        # goods.delete()

        # 逻辑删除，仅不显示和使用，数据库内还有
        goods.is_delete = 1
        goods.save()
        return redirect('shop:type_show')
    else:
        return render(request, 'type_show.html', {'msg': '删除失败！'})


def update(request):
    """
    用户信息修改
    :param request:
    :return:
    """
    if request.method == 'POST':
        id = request.POST.get('id')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        realname = request.POST.get('realname')
        address = request.POST.get('address')
        age = request.POST.get('age')
        job = request.POST.get('job')
        gender = request.POST.get('gender')
        is_delete = request.POST.get('is_delete')
        print(id, username, phone, email, password, realname, address, age, job, gender, is_delete)
        # 方式1
        # user = User.objects.get(pk=id)
        # user.username = username
        # user.phone = phone
        # # 字符串强制转换布尔类型
        # user.is_delete = bool(is_delete)
        # user.save()

        # 方式2
        # User.objects.filter(pk=id).update(username=username, phone=phone, is_delete=bool(is_delete))
        #     return redirect('shop:show')
        # else:
        #     id = request.GET.get('id')
        #     user = User.objects.get(pk=id)
        #     if user:
        #         return render(request, 'update.html', {'user': user})
        #     else:
        #         return redirect('shop:show')

        # ajax的post
        # result返回受影响的行数
        result1 = User.objects.filter(pk=id).update(username=username, phone=phone,
                                                    email=email, password=password, is_delete=is_delete)
        result2 = UserProfile.objects.filter(user_id=id).update(realname=realname, address=address, age=age,
                                                                gender=gender, job=job)
        if result1 == 1 and result2 == 1:
            return JsonResponse({'msg': '修改成功！'})
        else:
            return JsonResponse({'msg': '修改失败！'})
    else:
        id = request.GET.get('id')
        user = User.objects.get(pk=id)
        if user:
            return render(request, 'update.html', {'user': user})
        else:
            return redirect('shop:show')


def add_goods(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        weight = request.POST.get('weight')
        type_id = request.POST.get('type')

        goods = Goods.objects.create(name=name, desc=desc, price=price, weight=weight, type_id=type_id)
        # 可以由商品找类别的属性
        print(goods.type.tname)
        if goods:
            return HttpResponse('商品添加成功')
        else:
            return render(request, 'add_goods.html', {'msg': '添加失败！'})
    else:
        types = GoodsType.objects.all()
        return render(request, 'add_goods.html', {'types': types})


def type_show(request):
    """
    商品类别展示
    :param request:
    :return:
    """
    # types = Type.objects.filter(is_delete=0).all()
    # goodss = Goods.objects.filter(is_delete=0).all()
    types = GoodsType.objects.all()
    goodss = Goods.objects.all()
    return render(request, 'type_show.html', {'types': types, 'goodss': goodss})


# 使用get查找
def detail_type(request, tid):
    """
    根据类别id查找商品
    :param request:
    :param tid:
    :return:
    """
    type1 = GoodsType.objects.all()
    type2 = GoodsType.objects.get(pk=tid)
    return render(request, 'detail_type.html', {'types': type1, 'single_type': type2})


# 使用ajax查找分类
def type_search(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':

        tid = request.POST.get('tid')
        type = GoodsType.objects.get(pk=tid)
        typedict = {'tname': type.tname, 'add_time': type.add_time}
        goods = Goods.objects.filter(type_id=tid).values('name', 'desc', 'price', 'weight', 'store_num', 'sale_num',
                                                         'save_num')
        show_type = []
        goods = list(goods)
        for i in goods:
            show_type.append({**typedict, **i})
        return JsonResponse({'show_type': show_type})
    else:
        return render(request, 'type_show.html')


def goods_details(request, gid):
    """
    商品详情及一个同类新品推荐
    :param request:
    :param gid:
    :return:
    """
    types = GoodsType.objects.all()
    try:
        goods = Goods.objects.get(pk=gid)
    except:
        return redirect('shop:welcome')
    new_goods = Goods.objects.filter(goodstype=goods.goodstype).order_by('update_time')[:2]
    # 验证用户登录设置购物车状态
    count = 0
    if request.user.is_authenticated:
        count = Cart.objects.filter(new_user=request.user).count()
    return render(request, 'goods_details.html',
                  {'types': types, 'goods': goods, 'new_goods': new_goods, 'count': count})


def goods_collection(request):
    """
    商品收藏
    :param request:
    :return:
    """
    id = request.GET.get('id')
    flag = request.GET.get('flag')
    goods = Goods.objects.get(pk=id)
    if flag == '0':
        if goods:
            goods.save_num += 1
            goods.save()
            return JsonResponse({'msg': '收藏成功！', 'save_num': goods.save_num})
        else:
            return JsonResponse({'msg': '收藏失败！'})
    elif flag == '1':
        if goods:
            goods.save_num -= 1
            goods.save()
            return JsonResponse({'msg': '取消收藏成功！', 'save_num': goods.save_num})
        else:
            return JsonResponse({'msg': '取消收藏失败！'})


def delete_type(request):
    """
    删除类别, 删除类别下的商品
    :param request:
    :return:
    """
    tid = request.GET.get('id')
    type = GoodsType.objects.get(pk=tid)
    if type:
        # type.delete()  //如果在建立模型时没有设置保护，则会直接级联删除所有商品
        type.is_delete = 1
        type.save()
        goods = Goods.objects.filter(type_id=tid).update(is_delete=1)
        return render(request, 'type_show.html', {'msg': '删除成功！'})
    else:
        return render(request, 'type_show.html', {'msg': '删除失败！'})


def cart_add(request):
    """
    加入购物车
    :param request:
    :return:
    """
    gid = request.GET.get('id')
    goodsnum = request.GET.get('goodsnum')
    total = request.GET.get('total')

    # 判断商品是否添加过
    if Cart.objects.filter(goods_id=gid, new_user_id=request.user.id).count() > 0:
        cart = Cart.objects.get(goods_id=gid, new_user_id=request.user.id)
        cart.number += int(goodsnum)
        cart.total += decimal.Decimal(total)
        cart.save()
    else:
        cart = Cart.objects.create(goods_id=gid, new_user=request.user, number=goodsnum, total=float(total))
    if cart:
        count = Cart.objects.filter(new_user=request.user).count()
        return JsonResponse({'status': '添加成功！', 'count': count})
    else:
        return JsonResponse({'status': '添加失败！'})


def show_my_cart(request):
    """
    显示我的购物车    user.goods_set.all()
    商品被添加的用户  goods.user.all()
    :param request:
    :return:
    """
    carts = Cart.objects.filter(new_user=request.user).all()
    types = GoodsType.objects.all()
    return render(request, 'show_my_cart.html', {'types': types, 'carts': carts, })


def cart_del(request):
    """
    删除购物车中的商品
    :param request:
    :return:
    """
    gid = request.GET.get('gid')
    # 物理删除
    result = Cart.objects.filter(new_user=request.user, goods_id=gid).delete()
    if result:
        return redirect('/show_my_cart/')
    else:
        carts = Cart.objects.filter(new_user=request.user).all()
        types = GoodsType.objects.all()
        return render(request, 'show_my_cart.html', {'types': types, 'carts': carts, 'msg': '删除失败！'})


def cart_goods_adjust(request):
    gid = request.GET.get('gid')
    num = request.GET.get('num')
    total = request.GET.get('total')
    Cart.objects.filter(new_user=request.user, goods_id=gid).update(number=num, total=total)
    return JsonResponse({'msg': 'success'})


def register_exist(request):
    """
    检查用户名是否重复
    :param request:
    :return:
    """
    new_name = request.GET.get('username')
    username = User.objects.filter(username=new_name).first()
    if username:
        return JsonResponse({'count': 1})
    else:
        return JsonResponse({'count': 0})


def forget_password(request):
    """
    忘记密码修改
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 验证验证码
        phone = request.POST.get('phone')
        code = request.POST.get('verification_code')
        new_password = request.POST.get('password')
        # 在session里取值
        # if request.session.get(phone) == code:
        if cache.get(phone) == code:
            new_user = NewUser.objects.filter(phone=phone).first()
            new_password = make_password(password=new_password)
            new_user.password = new_password
            new_user.save()
            return render(request, 'login.html', {'msg': '密码修改成功！'})
        else:
            return render(request, 'forget_password.html', {'msg': '验证码错误！'})
    return render(request, 'forget_password.html', {'user': None})


def send_verification_code(request):
    """
    发送验证码
    :param request:
    :return:
    """
    if request.method == 'POST':
        phone = request.POST.get('phone')
        print(phone)
        # 使用第三方服务
        # 使用requests，其相对于浏览器
        import time
        url = 'https://api.netease.im/sms/sendcode.action'
        headers = {}
        Nonce = str(uuid.uuid4()).replace('-', '')
        AppSecret = '4697c32048a1'
        CurTime = str(time.time())
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        headers['AppKey'] = 'a7c29a24fe50997474bd9c504b85f9db'
        headers['Nonce'] = Nonce
        headers['CurTime'] = CurTime
        CheckSum = hashlib.sha1((AppSecret + Nonce + CurTime).encode('utf-8')).hexdigest()
        headers['CheckSum'] = CheckSum

        import requests
        response = requests.post(url=url, data={'mobile': phone}, headers=headers)

        json_result = response.json()

        if json_result.get('code') == 200:
            # 建立手机号和验证码的字典关系
            # 放入session
            # request.session[phone] = json_result.get('obj')

            # 放入redis缓存
            cache.set(phone, json_result.get('obj'))

            return JsonResponse({'msg': '验证码发送成功'})
        else:
            return JsonResponse({'msg': '验证码发送失败'})
    return render(request, 'forget_password.html')


def upload_icon(request):
    """
    更换用户头像
    :param request:
    :return:
    """
    uid = request.POST.get('uid')
    icon = request.FILES.get('icon')
    new_user = NewUser.objects.get(pk=uid)
    new_user.icon = icon
    new_user.save()
    return JsonResponse({'msg': 'ok', 'img_path': str(new_user.icon)})


# def receive_address(request):
#     return render(request, 'receive_address.html')
#
#
# def order(request):
#     return render(request, 'order.html')


def generate_order(request):
    """
    生成订单
    :param request:
    :return:
    """
    # 获得选择的商品id列表
    gid_list = request.POST.getlist('selected_1')

    if not gid_list:
        return redirect('shop:show_my_cart')
    # 商品对象列表
    goods_list = []
    # 商品种类数量
    all_numbers = 0
    # 商品总价格
    all_total = 0
    # 获取购物车中要结算的商品信息
    for gid in gid_list:
        cart = Cart.objects.get(goods_id=gid, new_user=request.user)
        goods = Goods.objects.get(pk=gid)
        goods.number = cart.number
        goods.total = cart.total

        goods_list.append(goods)

        all_numbers += 1
        all_total += cart.total
    # 运费
    carriage_price = 10
    # 实付款=总价格+运费
    real_total = all_total + carriage_price

    # 收货地址
    addrs = Address.objects.filter(new_user=request.user)

    goods_list_str = ','.join(gid_list)

    return render(request, 'place_order.html', locals())


def submit_order(request):
    """
    提交订单
    :param request:
    :return:
    """
    if request.method == 'POST':
        addrid = request.POST.get('addrid')
        pay_method = request.POST.get('pay_method')
        gid_list_str = request.POST.get('gid_list_str')
        real_total = request.POST.get('real_total')
        carriage_price = request.POST.get('carriage_price')
        all_numbers = request.POST.get('all_numbers')
        print(addrid, pay_method, gid_list_str, real_total, carriage_price, all_numbers)
        # 对多个值判断是否存在
        if not all([addrid, pay_method, gid_list_str]):
            return JsonResponse({'status': '401', 'msg': '不完整'})
        # 创建订单
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(request.user.id)

        # 设置事务保存点
        from django.db import transaction
        save_id = transaction.savepoint()
        try:
            order = Order.objects.create(order_id=order_id, new_user=request.user, address_id=addrid,
                                         pay_method=pay_method, goods_num=all_numbers, goods_total=real_total,
                                         carriage_price=carriage_price)

            gid_list = gid_list_str.split(',')

            for gid in gid_list:

                try:
                    # 获取购物车商品
                    cart = Cart.objects.get(goods_id=gid, new_user=request.user)
                    # 获取商品对象
                    goods = Goods.objects.get(pk=gid)
                except:
                    # 商品不存在
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'status': '401', 'msg': '商品不存在'})
                # 判断商品数量是否大于库存量
                if cart.number > goods.store_num:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'status': '401', 'msg': '库存不足'})
                # 添加订单商品
                OrderGoods.objects.create(order=order, goods_id=gid, number=cart.number, price=cart.total)
                # 修改库存
                goods.store_num -= cart.number
                # 修改销售量
                goods.sale_num += cart.number
                goods.save()

                # 删除购物车
                cart.delete()
        except Exception as err:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'status': '401', 'msg': '下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        return JsonResponse({'status': '200', 'msg': '下单成功'})


def order_pay(request):
    """
    订单支付
    :param request:
    :return:
    """
    order_id = request.POST.get("order_id")
    pay_method = request.POST.get("pay_method")
    if not order_id:
        return JsonResponse({"status": "401", 'msg': '订单号无效'})
    try:
        order = Order.objects.get(new_user=request.user, order_id=order_id, pay_method=pay_method, )
    except:
        return JsonResponse({'status': '401', 'msg': '订单错误'})

    # 接入支付宝

    app_private_key_string = open(settings.PRIVATE_KEY).read()
    alipay_public_key_string = open(settings.PUBLIC_KEY).read()

    alipay = AliPay(
        # 测试用沙箱appid，上线使用应用的appid
        appid="2021000119665566",
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认 False
        verbose=False,  # 输出调试数据
        config=AliPayConfig(timeout=15)  # 可选，请求超时时间
    )
    subject = "便利鲜fruitshop商品购买" + str(order_id)

    # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 交易码
        total_amount=str(order.goods_total),  # 总金额字符串的
        subject=subject,  # 主题
        return_url=None,
        notify_url=None  # 可选，不填则使用默认 notify url
    )

    # 沙箱网关和应用的不一样
    url = 'https://openapi.alipaydev.com/gateway.do?'

    # 组成支付地址
    path = url + order_string

    return JsonResponse({'status': '200', 'pay_path': path})


def check_order(request):
    """
    订单状态检查
    :param request:
    :return:
    """
    order_id = request.POST.get("order_id")
    if not order_id:
        return JsonResponse({"status": "401", 'msg': '订单号无效'})

    try:
        order = Order.objects.get(new_user=request.user, order_id=order_id, )
    except:
        return JsonResponse({'status': '401', 'msg': '订单错误'})
        # 接入支付宝

    app_private_key_string = open(settings.PRIVATE_KEY).read()
    alipay_public_key_string = open(settings.PUBLIC_KEY).read()

    alipay = AliPay(
        # 测试用沙箱appid，上线使用应用的appid
        appid="2021000119665566",
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认 False
        verbose=False,  # 输出调试数据
        config=AliPayConfig(timeout=15)  # 可选，请求超时时间
    )

    while True:
        # 返回支付结果
        response = alipay.api_alipay_trade_query(order_id)
        # 查询状态码和交易状态状态
        code = response.get('code')  # 支付宝接口调用状态10000表示成功，40004表示失败
        trade_status = response.get('trade_status')  # 交易状态

        # 判断
        if code == '10000' and trade_status == "TRADE_SUCCESS":
            # 交易码
            trade_on = response.get("trade_on")
            order.trade_on = trade_on
            # 设置订单状态
            order.order_status = 2
            return JsonResponse({'status': '200', 'msg': '支付成功'})
        elif code == '40004' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
            # 等待支付
            import time
            time.sleep(5)
        else:
            return JsonResponse({'status': '401', 'msg': '付款失败'})


def order_comment(request):
    # 取购物车
    count = Cart.objects.filter(new_user=request.user).count()
    if request.method == 'POST':
        orderid = request.POST.get('order_id')
        if not orderid:
            return redirect('shop:detail')
        try:
            order = Order.objects.get(new_user=request.user, order_id=orderid)
        except:
            return redirect(reverse('shop:detail'))

        goods_num = int(request.POST.get('goods_num'))
        for i in range(1, goods_num + 1):
            goods_id = request.POST.get('goods_' + str(i))
            comment = request.POST.get('content_' + str(i))

            ordergoods = OrderGoods.objects.get(order_id=orderid, goods_id=goods_id)
            ordergoods.comment = comment
            ordergoods.save()

        order.order_status = 5
        order.save()
        return redirect(reverse('shop:detail'))

    else:
        orderid = request.GET.get('orderid')
        if not orderid:
            return redirect('shop:detail')
        try:
            order = Order.objects.get(new_user=request.user, order_id=orderid)
        except:
            return redirect(reverse('shop:detail'))

        for status in Order.ORDER_STATUS:
            if order.order_status in status:
                order.status = status[1]
                break
        for pay_method in Order.PAY_METHODS:
            if order.pay_method in pay_method:
                order.paymethod = pay_method[1]
                break
        return render(request, 'order_comment.html', {'order': order, 'count': count})
