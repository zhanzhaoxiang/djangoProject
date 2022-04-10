from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from openpyxl.styles.builtins import total


class User(models.Model):
    """
    用户常用信息
    """
    username = models.CharField(max_length=100, unique=True, null=False, blank=False,
                                error_messages={'unique': '用户名重复'})
    password = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    add_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        # 指定表名
        db_table = 'user'


class UserProfile(models.Model):
    """
    用户详细信息
    """
    realname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    job = models.CharField(max_length=50)
    gender = models.CharField(max_length=5, choices=(('boy', '男'), ('girl', '女')))

    # 用户常用信息与用户详细信息一对一,on_delete=models.PROTECT,级联受保护，不能随便删除;on_delete=models.CASCADE直接级联删除
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    class Meta:
        # 指定表名
        db_table = 'userprofile'


class NewUser(AbstractUser):
    """
    另一种创建用户方式，已经集成了一些方法属性，verbose_name是给admin管理后台看的
    """
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号码")
    # 头像，用ImageField上传图片,用FileField上传文件，在media文件夹下自动创建uploads/%Y/%m/%d文件夹
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d', default='media/default.png', verbose_name='头像')

    class Meta:
        db_table = 'newuser'

        # 设置后台表名
        verbose_name = '新用户表'
        # 会自动在表名后面添加s，这样设置后台表名就不会显示s了
        verbose_name_plural = verbose_name


class Address(models.Model):
    """
    收货地址表
    """
    receive_user = models.CharField(max_length=100, verbose_name='收件人')
    receive_address = models.CharField(max_length=256, verbose_name='收件地址')
    post_code = models.CharField(max_length=6, verbose_name='邮编')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')
    phone = models.CharField(max_length=11, verbose_name='联系号码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    new_user = models.ForeignKey(to=NewUser, on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = 'address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name


class BaseModel(models.Model):
    """
    基本类
    """
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True  # 声明应该父类，不会添加到数据库


class GoodsType(BaseModel):
    """
    商品类型
    """
    tname = models.CharField(max_length=200, verbose_name='类别名称')
    logo = models.CharField(max_length=200, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='类别图片')

    def __str__(self):
        return self.tname

    class Meta:
        db_table = 'goodstype'
        verbose_name = '商品类别表'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    """
    商品
    """
    name = models.CharField(max_length=100, verbose_name='商品名称')
    desc = models.CharField(max_length=250, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')  # 价格总长度6位，小数2位，float类型长度不确定
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    store_num = models.IntegerField(default=100, verbose_name='商品库存')
    sale_num = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, verbose_name='商品状态', choices=((0, '下线'), (1, '上线')))

    # 建立1对多关系
    goodstype = models.ForeignKey(to=GoodsType, verbose_name='商品种类', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    """
    商品图片
    """
    goods = models.ForeignKey(to=Goods, verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class Cart(BaseModel):
    new_user = models.ForeignKey(to=NewUser, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name='商品')
    number = models.IntegerField(verbose_name='商品数量')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价格')

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.new_user.username


class IndexGoodsBanner(BaseModel):
    """
    首页轮播图片
    """
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name='商品图片')
    index = models.SmallIntegerField(default=0, verbose_name='显示顺序')

    class Meta:
        db_table = 'index_banner'
        verbose_name = '首页轮播图片'
        verbose_name_plural = verbose_name


class IndexGoodsTypeBanner(BaseModel):
    """
    首页分类展示商品表
    """
    goods = models.ForeignKey(to=Goods, verbose_name='广告商品', on_delete=models.CASCADE, null=True)
    goodstype = models.ForeignKey(to=GoodsType, verbose_name='商品种类', on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(default=1, choices=((0, '标题'), (1, '图片')), verbose_name='显示类型')
    index = models.SmallIntegerField(default=0, verbose_name='显示顺序')

    class Meta:
        db_table = 'index_goods_type'
        verbose_name = '首页分类展示商品表'
        verbose_name_plural = verbose_name


class IndexSaleBanner(BaseModel):
    name = models.CharField(max_length=100, verbose_name='促销活动名称')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='显示顺序')
    url = models.URLField(verbose_name='活动链接')

    class Meta:
        db_table = 'index_sale'
        verbose_name = '首页促销活动'
        verbose_name_plural = verbose_name
