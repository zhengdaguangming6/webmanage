from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from apps.bug import models
from common import return_code
from apps.bug.mixins.bug_list import (BugCreateModelMixin, BugDestroyModelMixin, BugUpdateModelMixin, BugListModelMixin,
                                      BugRetrieveModelMixin, BugPushMessageUpdateModelMixin)
from apps.bug.serializers.bug_list import BugSerializer
from apps.bug.extension.page import BugPageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from apps.bug.extension.filter_setting import BugFilterset


class BugView(BugCreateModelMixin, BugDestroyModelMixin, BugUpdateModelMixin, BugListModelMixin, BugRetrieveModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = BugFilterset

    queryset = models.BugList.objects.filter(status=1).order_by("-id")
    serializer_class = BugSerializer
    pagination_class = BugPageNumberPagination

    # 把post请求的传参保存到数据库
    def perform_create(self, serializer):
        # 保存创建人的uid和更新人uid
        serializer.save(create_user_id=self.request.user.user_id, update_user_id=self.request.user.user_id)
        result = {"code": return_code.SUCCESS, "msg": "保存成功", "data": serializer.data}
        return Response(result)

    # 全局更新 put
    def perform_update(self, serializer):
        serializer.save(update_user_id=self.request.user.user_id)

    # 局部更新 patch
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class BugPushMessageView(BugPushMessageUpdateModelMixin, GenericViewSet):
    queryset = models.BugList.objects.filter(status=1).order_by("-id")
    serializer_class = BugSerializer

    # 全局更新 put
    def perform_update(self, serializer):
        serializer.save(update_user_id=self.request.user.user_id)

    # 局部更新 patch
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
