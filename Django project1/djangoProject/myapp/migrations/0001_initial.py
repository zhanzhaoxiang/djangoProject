# Generated by Django 4.0.3 on 2022-04-16 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, verbose_name='用户类型')),
            ],
            options={
                'verbose_name': '用户类型表',
                'verbose_name_plural': '用户类型表',
                'db_table': 'user_type',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('email', models.CharField(max_length=50, verbose_name='邮箱')),
                ('address', models.CharField(choices=[('中国', '中国'), ('美国', '美国'), ('俄国', '俄国')], max_length=30, verbose_name='国家')),
                ('is_super', models.BooleanField(default=False, verbose_name='是否是管理员')),
                ('usertype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.usertype')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user',
            },
        ),
    ]
