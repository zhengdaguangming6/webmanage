from django.db import models


class UserInfo(models.Model):
    STATUS_CHOICES = (
        (0, "已删除"),
        (1, "正常"),
    )
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, null=True)
    status = models.SmallIntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = "user_info"
        verbose_name = "用户信息"