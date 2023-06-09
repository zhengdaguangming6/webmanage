# Generated by Django 3.2 on 2023-04-23 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('status', models.SmallIntegerField(choices=[(0, '已删除'), (1, '正常')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '用户信息',
                'db_table': 'user_info',
            },
        ),
    ]
