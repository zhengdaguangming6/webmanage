from django.db import models
from apps.user.models import UserInfo


class BugList(models.Model):
    PRIORITY_CHOICES = (
        ("a", "紧急"),
        ("b", "高"),
        ("c", "中"),
        ("d", "低"),
    )
    LEVEL_CHOICES = (
        ("a", "致命"),
        ("b", "严重"),
        ("c", "一般"),
        ("d", "轻微"),
    )
    CLASSIFICATION_CHOICES = (
        (0, "功能"),
        (1, "界面"),
        (2, "兼容性"),
        (3, "易用性"),
        (4, "安全性"),
        (5, "性能"),
        (6, "服务器配置"),
        (7, "DB"),
        (8, "其他"),
    )
    CAUSE_CHOICES = (
        (0, "需求不清晰"),
        (1, "代码设计缺陷"),
        (2, "代码错误"),
        (3, "环境问题"),
        (4, "运营配置问题"),
        (5, "用户理解有歧义"),
        (6, "大数据相关"),
        (7, "其他"),
    )
    DEPARTMENT_CHOICES = (
        (0, "需求问题"),
        (1, "iOS"),
        (2, "安卓"),
        (3, "server端"),
        (4, "管理后台"),
        (5, "web官网"),
        (6, "活动页面"),
        (7, "app内H5"),
        (8, "小程序"),
        (9, "算法"),
        (10, "大数据"),
        (11, "运营"),
        (12, "其他"),
    )
    RESULT_CHOICES = (
        (0, "待处理"),
        (1, "处理中"),
        (2, "不是bug"),
        (3, "无法复现"),
        (4, "没找到原因，持续观察"),
        (5, "后续解决"),
        (6, "已解决"),
        (7, "下一版本修复"),

    )
    STATUS_CHOICES = (
        (0, "已删除"),
        (1, "正常"),
    )
    IS_PUSH_CHOICES = (
        (0, "未发送"),
        (1, "已发送"),
    )
    submitter = models.CharField(verbose_name="提交问题人", max_length=64)
    content = models.CharField(verbose_name="问题描述", max_length=1000)
    priority = models.CharField(verbose_name="问题优先级", max_length=2, default="c", choices=PRIORITY_CHOICES)
    level = models.CharField(verbose_name="问题等级", max_length=2, default="c", choices=LEVEL_CHOICES)
    classification = models.SmallIntegerField(verbose_name="问题分类", default=8, choices=CLASSIFICATION_CHOICES)
    cause = models.SmallIntegerField(verbose_name="引入原因", default=7, choices=CAUSE_CHOICES)
    department = models.SmallIntegerField(verbose_name="问题所属端", default=12, choices=DEPARTMENT_CHOICES)
    result = models.SmallIntegerField(verbose_name="问题处理结果", default=0, choices=RESULT_CHOICES)
    follow_up_person = models.CharField(verbose_name="问题跟进人", max_length=10, null=True)
    solver = models.CharField(verbose_name="问题处理人", max_length=10, null=True)
    cause_detail = models.CharField(verbose_name="问题具体原因", max_length=1000, null=True)
    is_push = models.SmallIntegerField(verbose_name="是否已发送到钉钉", default=0, choices=IS_PUSH_CHOICES)
    at_persons = models.CharField(verbose_name="@相关人员", max_length=200, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    create_user = models.ForeignKey(verbose_name="创建人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING,
                                    related_name="bug_create_user")
    update_user = models.ForeignKey(verbose_name="更新人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING,
                                    related_name="bug_update_user")
    status = models.SmallIntegerField(verbose_name="该条记录状态", default=1)

    class Meta:
        db_table = "bug_list"
        verbose_name = "线上bug记录"


class RobotList(models.Model):
    title = models.CharField(verbose_name="项目名称", max_length=64)
    secret = models.CharField(verbose_name="加签", max_length=64)
    access_token = models.CharField(verbose_name="令牌", max_length=64)
    push_time = models.CharField(verbose_name="发送时间", max_length=128)
    at_persons = models.CharField(verbose_name="@相关人员", max_length=64)
    msg = models.CharField(verbose_name="下发内容", max_length=2000)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    create_user = models.ForeignKey(verbose_name="创建人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING,
                                    related_name="robot_create_user")
    update_user = models.ForeignKey(verbose_name="更新人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING,
                                    related_name="robot_update_user")

    class Meta:
        db_table = "robot_list"
        verbose_name = "机器人列表"