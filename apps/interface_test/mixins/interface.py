#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework import mixins
from rest_framework.response import Response
from common import return_code


class InterfaceCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        receive_data = request.data
        for key in list(receive_data.keys()):
            if not receive_data[key]:
                print("删除穿惨中值是空字符串%%%%%%%%%%%%%%%%=============================================", key)

                receive_data.pop(key)
        serializer = self.get_serializer(data=receive_data)
        print("serializer接口记录------", type(serializer), serializer)
        # 1.异常处理
        if not serializer.is_valid():
            result = {"code": return_code.VALIDATE_ERROR, "detail": serializer.errors, "msg": "保存失败,请检查传参"}
            return Response(result)

        # 2.优化perform_create保存数据
        res = self.perform_create(serializer)
        # 3.返回数据的处理
        return res or Response({"code": return_code.SUCCESS, "data": serializer.data})


class InerfaceDestroyModelMixin(mixins.DestroyModelMixin):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=False)
        res = self.perform_destroy(instance)

        return res or Response({"code": return_code.SUCCESS, "msg": "删除成功", "data": serializer.data})


class InterfaceUpdateModelMixin(mixins.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        none_data = {}
        receive_data = request.data
        for key in list(receive_data.keys()):
            if not receive_data[key]:
                print("删除穿惨中值是空字符串%%%%%%%%%%%%%%%%=============================================", key)
                val = receive_data.pop(key)
                none_data[key] = val
        print("none_data============", type(none_data), none_data)
        print("receive_data===============", type(receive_data), receive_data)

        serializer = self.get_serializer(instance, data=receive_data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        print("none_data======", none_data)
        if not serializer.is_valid():
            result = {"code": return_code.VALIDATE_ERROR, "detail": serializer.errors, "msg": "保存失败,请检查传参"}
            return Response(result)

        res = self.perform_update(serializer, **none_data)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return res or Response({"code": return_code.SUCCESS, "msg": "更新成功", "data": serializer.data})


class InterfaceListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        # keys = ["params", "data", "json", "headers"]
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # res_data = serializer.data
            # for dict_data in res_data:
            #     for key in keys:
            #         if not dict_data.get(key):
            #             # 删除值是空字符串的键值对
            #             dict_data.pop(key)
            #         else:
            #             # 把字符串格式变为字典格式
            #             dict_data[key] = json.loads(dict_data[key])

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # result_data = serializer.data
        # for dict_data in result_data:
        #     for key in keys:
        #         if not dict_data.get(key):
        #             # 删除值是空字符串的键值对
        #             dict_data.pop(key)
        #         else:
        #             # 把字符串格式变为字典格式
        #             dict_data[key] = json.loads(dict_data[key])
        return Response({"code": return_code.SUCCESS, "data": serializer.data})


class InterfaceRetrieveModelMixin(mixins.RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": return_code.SUCCESS, "msg": "查询单条数据成功", "data": serializer.data})




