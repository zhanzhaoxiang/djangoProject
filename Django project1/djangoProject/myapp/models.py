from django.db import models


# Create your models here.


class UserType(models.Model):
    type_name = models.CharField(max_length=50, verbose_name='用户类型')

    class Meta:
        db_table = 'user_type'
        verbose_name = '用户类型表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class User(models.Model):
    """
    用户常用信息
    """
    username = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=100, null=False, blank=False, verbose_name='密码')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    email = models.CharField(max_length=50, verbose_name='邮箱')
    country = models.CharField(max_length=30, choices=(('中国', '中国'), ('美国', '美国'), ('俄国', '俄国')), verbose_name='国家')
    is_super = models.BooleanField(default=False, verbose_name='是否是管理员')
    usertype = models.ForeignKey(to=UserType, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        # 指定表名
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
