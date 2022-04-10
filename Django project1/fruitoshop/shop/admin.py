from celery.bin.celery import list_
from django.contrib import admin
from .models import *


# 自定义站点设置
class MyAdminSite(admin.AdminSite):
    site_header = '便利鲜商城'
    site_title = 'Fruit Shop'
    index_title = 'Fruit 商城'


# 自定义admin管理员
admin_site = MyAdminSite(name='myadmin')


# 设置要显示的字段
class NewUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name', 'date_joined']
    list_per_page = 10  # 每页显示10条数据
    ordering = ('-date_joined',)  # 按照时间降序排列
    list_editable = ['phone', 'first_name', 'last_name']  # 可以编辑的字段
    list_filter = ['phone', 'date_joined']  # 过滤器
    search_fields = ['username', 'phone']  # 搜索字段
    date_hierarchy = 'date_joined'  # 详细时间分层筛选


class AddressAdmin(admin.ModelAdmin):
    list_display = ['receive_user', 'receive_address', 'phone']


class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['tname', 'logo']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['goodstype', 'name', 'price', 'store_num', 'sale_num', 'status']


class IndexGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['goods', 'index']


class IndexGoodsTypeBannerAdmin(admin.ModelAdmin):
    list_display = ['goodstype', 'display_type', 'index']


class IndexSaleBannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'index', 'url']


class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ['goods']


class CartAdmin(admin.ModelAdmin):
    list_display = ['new_user', 'goods','number','total']

# Register your models here.
# 使用默认admin配置注册
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexGoodsTypeBanner, IndexGoodsTypeBannerAdmin)
admin.site.register(IndexSaleBanner, IndexSaleBannerAdmin)

admin.site.site_header = '便利鲜商城'
admin.site.site_title = 'Fruit Shop'
admin.site.index_title = 'Fruit 商城'

# 使用自定义admin配置注册
# admin_site.register(NewUser, NewUserAdmin)
