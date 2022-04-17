from django.urls import path, re_path, include

from . import views

app_name = 'myapp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('valid/', views.valid, name='valid'),
    path('login1/', views.login1, name='login1'),
    path('draw/', views.draw, name='draw'),
]
