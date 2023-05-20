#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework import routers
from apps.interface_test.views import interface, requestor

router = routers.SimpleRouter()

# 接口测试视图 Interface视图
router.register(r'interface', interface.InterfaceView)

# 发送接口Requestor视图
router.register(r'requestor', requestor.RequestorView)

# 测试报告一级列表
router.register(r'requestor_report_primary', requestor.RequestorReportPrimaryView)


urlpatterns = [
    # path('register/', account.RegisterView.as_view({"post": "create"})),
    # path('auth/', account.AuthView.as_view()),
    # 批量接口测试
    path('requestor_many/', requestor.RequestorManyView.as_view(), name="requestor_many")
]

urlpatterns += router.urls