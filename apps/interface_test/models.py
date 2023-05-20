from django.db import models
from apps.user.models import UserInfo


class InterfaceTest(models.Model):
    STATUS_CHOICES = (
        (0, "已删除"),
        (1, "正常"),
    )
    RUN_CHOICES = (
        (0, "不执行"),
        (1, "执行"),
    )
    interface_title = models.CharField(verbose_name="接口名称", max_length=64, default="请输入接口名称")
    method = models.CharField(verbose_name="请求方法", max_length=10)
    path = models.CharField(verbose_name="接口", max_length=64)
    domain = models.CharField(verbose_name="域名", max_length=20)
    params = models.CharField(verbose_name="get请求传的参数", max_length=500, null=True)
    data = models.CharField(verbose_name="post请求发送表单数据", max_length=500, null=True)
    json = models.CharField(verbose_name="post请求发送json数据", max_length=500, null=True)
    headers = models.CharField(verbose_name="请求头", max_length=1000, null=True)
    status = models.SmallIntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=1)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, null=True)
    create_user = models.ForeignKey(verbose_name="创建人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING, related_name="create_user")
    update_user = models.ForeignKey(verbose_name="更新人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING, related_name="update_user")
    notes = models.TextField(verbose_name="备注", null=True)
    run = models.SmallIntegerField(verbose_name="是否执行", default=1)
    asserts = models.CharField(verbose_name="断言", max_length=500, null=True)
    username = models.CharField(verbose_name="当前接口执行之前登录的用户名", max_length=32, null=True)
    phone = models.CharField(verbose_name="当前接口执行之前登录的手机号", max_length=20, default=0)
    password = models.CharField(verbose_name="当前接口执行之前登录的密码", max_length=100, default=0)

    class Meta:
        db_table = "interface_test"
        verbose_name = "接口记录"


class Requestor(models.Model):
    RESULT_CHOICES = (
        (0, "已删除"),
        (1, "正常"),
    )
    task_title = models.CharField(verbose_name="任务名称", max_length=30)
    task_env = models.CharField(verbose_name="运行环境", max_length=30)
    pro_title = models.CharField(verbose_name="项目名称", max_length=30)
    content = models.TextField(verbose_name="请求返回数据")
    status = models.SmallIntegerField(verbose_name="状态：正常/已删除", choices=RESULT_CHOICES)
    create_user = models.ForeignKey(verbose_name="创建人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING, related_name="c_user")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)

    class Meta:
        db_table = "requestor"
        verbose_name = "接口测试结果"
