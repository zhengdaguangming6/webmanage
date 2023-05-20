#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from apps.interface_test import models
from common import return_code
from apps.interface_test.mixins.interface import\
    (InterfaceCreateModelMixin, InterfaceListModelMixin, InerfaceDestroyModelMixin,
    InterfaceUpdateModelMixin, InterfaceRetrieveModelMixin
    )

from apps.interface_test.serializers.interface import InterfaceSerializer, InterfaceRetrieveSerializer
from apps.interface_test.extension.page import InterfacePageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from apps.interface_test.extension.filter_setting import InterfaceFilterset



class InterfaceView(InterfaceCreateModelMixin, InterfaceListModelMixin, InterfaceRetrieveModelMixin, InerfaceDestroyModelMixin, InterfaceUpdateModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = InterfaceFilterset

    queryset = models.InterfaceTest.objects.filter(status=1).order_by("-id")
    serializer_class = InterfaceSerializer
    pagination_class = InterfacePageNumberPagination

    # 把post请求的传参保存到数据库
    def perform_create(self, serializer):
        # 保存创建人的uid和更新人uid
        serializer.save(create_user_id=self.request.user.user_id, update_user_id=self.request.user.user_id)
        # serializer.save(notes="这是主食主食注释")

        result = {"code": return_code.SUCCESS, "msg": "保存成功", "data": serializer.data}
        return Response(result)

    # 把某一条数据status改成0，作为逻辑删除
    def perform_destroy(self, instance):
        instance.status = 0
        instance.update_user_id = self.request.user.user_id   #
        print("这是更新用户uid", self.request.user.user_id)
        instance.save()

    # 全剧更新 put
    def perform_update(self, serializer, **kwargs):
        serializer.save(update_user_id=self.request.user.user_id)
        serializer.save(**kwargs)

    # 局部更新 patch
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # 给不同的请求方法用不同的序列化类
    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        if self.request.method == "GET":
            return InterfaceRetrieveSerializer

        return self.serializer_class

