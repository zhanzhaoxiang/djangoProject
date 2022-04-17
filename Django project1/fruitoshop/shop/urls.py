from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('register_exist/', views.register_exist, name="register_exist"),
    path('register/', views.register, name="register"),
    path('user_active/', views.user_active, name="user_active"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('forget_password/', views.forget_password, name="forget_password"),
    path('detail/', views.detail, name="detail"),
    path('show/', views.show, name="show"),
    path('delete/', views.delete, name="delete"),
    path('delete_goods/', views.delete_goods, name="delete_goods"),
    path('delete_type/', views.delete_type, name="delete_type"),
    path('update/', views.update, name="update"),
    path('upload_icon/', views.upload_icon, name="upload_icon"),
    path('add_goods/', views.add_goods, name="add_goods"),
    path('type_show/', views.type_show, name="type_show"),
    path('detail_type/<int:tid>', views.detail_type, name="detail_type"),
    path('type_search/', views.type_search, name="type_search"),
    path('goods_details/<int:gid>', views.goods_details, name="goods_details"),
    path('goods_collection/', views.goods_collection, name="goods_collection"),
    path('cart_add/', views.cart_add, name="cart_add"),
    path('show_my_cart/', views.show_my_cart, name="show_my_cart"),
    path('cart_del/', views.cart_del, name="cart_del"),
    path('cart_goods_adjust/', views.cart_goods_adjust, name="cart_goods_adjust"),
    path('send_verification_code/', views.send_verification_code, name="send_verification_code"),
    path('generate_order/', views.generate_order, name="generate_order"),
    path('submit_order/', views.submit_order, name="submit_order"),
    path('order_pay/', views.order_pay, name="order_pay"),
    path('check_order/', views.check_order, name="check_order"),
    path('order_comment/', views.order_comment, name="order_comment"),
]
