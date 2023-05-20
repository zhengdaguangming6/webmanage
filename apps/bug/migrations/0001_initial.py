# Generated by Django 3.2 on 2023-05-17 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BugList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitter', models.CharField(max_length=64, verbose_name='提交问题人')),
                ('content', models.CharField(max_length=1000, verbose_name='问题描述')),
                ('priority', models.CharField(choices=[('a', '紧急'), ('b', '高'), ('c', '中'), ('d', '低')], default='c', max_length=2, verbose_name='问题优先级')),
                ('level', models.CharField(choices=[('a', '致命'), ('b', '严重'), ('c', '一般'), ('d', '轻微')], default='c', max_length=2, verbose_name='问题等级')),
                ('classification', models.SmallIntegerField(choices=[(0, '功能'), (1, '界面'), (2, '兼容性'), (3, '易用性'), (4, '安全性'), (5, '性能'), (6, '服务器配置'), (7, 'DB'), (8, '其他')], default=8, verbose_name='问题分类')),
                ('cause', models.SmallIntegerField(choices=[(0, '需求不清晰'), (1, '代码设计缺陷'), (2, '代码错误'), (3, '环境问题'), (4, '运营配置问题'), (5, '用户理解有歧义'), (6, '大数据相关'), (7, '其他')], default=7, verbose_name='引入原因')),
                ('department', models.SmallIntegerField(choices=[(0, '需求问题'), (1, 'iOS'), (2, '安卓'), (3, 'server端'), (4, '管理后台'), (5, 'web官网'), (6, '活动页面'), (7, 'app内H5'), (8, '小程序'), (9, '算法'), (10, '大数据'), (11, '运营'), (12, '其他')], default=12, verbose_name='问题所属端')),
                ('result', models.SmallIntegerField(choices=[(0, '待处理'), (1, '处理中'), (2, '不是bug'), (3, '无法复现'), (4, '没找到原因，持续观察'), (5, '后续解决'), (6, '已解决'), (7, '下一版本修复')], default=0, verbose_name='问题处理结果')),
                ('follow_up_person', models.CharField(max_length=10, null=True, verbose_name='问题跟进人')),
                ('solver', models.CharField(max_length=10, null=True, verbose_name='问题处理人')),
                ('cause_detail', models.CharField(max_length=1000, null=True, verbose_name='问题具体原因')),
                ('is_push', models.SmallIntegerField(choices=[(0, '未发送'), (1, '已发送')], default=0, verbose_name='是否已发送到钉钉')),
                ('at_persons', models.CharField(max_length=200, null=True, verbose_name='@相关人员')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='该条记录状态')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_create_user', to='user.userinfo', verbose_name='创建人uid')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_update_user', to='user.userinfo', verbose_name='更新人uid')),
            ],
            options={
                'verbose_name': '线上bug记录',
                'db_table': 'bug_list',
            },
        ),
    ]
