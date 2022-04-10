# Generated by Django 4.0.3 on 2022-04-10 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_indexgoodstypebanner_display_type_goodsimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('number', models.IntegerField(verbose_name='商品数量')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='总价格')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.goods', verbose_name='商品')),
                ('new_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车表',
                'verbose_name_plural': '购物车表',
                'db_table': 'cart',
            },
        ),
    ]
