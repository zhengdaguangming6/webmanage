from rest_framework import mixins
from rest_framework.response import Response
from common import return_code
from utils.send_message.dingding.dingding import DingDingRobot
from utils.send_message.dingding.dingding_config import BUG_ROBOT
from apps.bug.models import BugList



class BugCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        receive_data = request.data
        for key in list(receive_data.keys()):
            if not receive_data[key]:
                print("删除穿参中 值是空字符串%%%%%%%%%%%%%%%%=============================================", key)
                receive_data.pop(key)
        serializer = self.get_serializer(data=receive_data)
        # 1.异常处理
        if not serializer.is_valid():
            result = {"code": return_code.VALIDATE_ERROR, "detail": serializer.errors, "msg": "保存失败,请检查传参"}
            return Response(result)

        # 2.优化perform_create保存数据
        res = self.perform_create(serializer)
        # 3.返回数据的处理
        return res or Response({"code": return_code.SUCCESS, "data": serializer.data})


class BugDestroyModelMixin(mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=False)
        res = self.perform_destroy(instance)
        return res or Response({"code": return_code.SUCCESS, "msg": "删除成功", "data": serializer.data})

    # 把某一条数据status改成0，作为逻辑删除
    def perform_destroy(self, instance):
        instance.status = 0
        instance.update_user_id = self.request.user.user_id  # 重写更新用户id
        print("这是更新用户uid", self.request.user.user_id)
        instance.save()


class BugUpdateModelMixin(mixins.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            result = {"code": return_code.VALIDATE_ERROR, "detail": serializer.errors, "msg": "修改失败,请检查传参"}
            return Response(result)

        res = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return res or Response({"code": return_code.SUCCESS, "msg": "更新成功", "data": serializer.data})


class BugListModelMixin(mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({"code": return_code.SUCCESS, "data": serializer.data})


class BugRetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    查看单条数据
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": return_code.SUCCESS, "msg": "查询单条数据成功", "data": serializer.data})


class BugPushMessageUpdateModelMixin(mixins.UpdateModelMixin):
    # 给@相关人发送钉钉消息---bug原因详情等信息
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            result = {"code": return_code.VALIDATE_ERROR, "detail": serializer.errors, "msg": "发送消息失败,请检查传参"}
            return Response(result)

        res = self.perform_update(serializer)
        bug_push_robot = DingDingRobot()
        msg = "BUG结果反馈\n问题提交人：{submitter}\n问题描述：{content}\n问题原因详情：{cause_detail}\n问题值班人：{follow_up_person}\n问题处理人：{solver}\n问题处理结果：{result}".format(
            submitter=serializer.data["submitter"],
            content=serializer.data["content"],
            cause_detail=serializer.data["cause_detail"],
            follow_up_person=serializer.data["follow_up_person"],
            solver=serializer.data["solver"],
            result=BugList.RESULT_CHOICES[serializer.data["result"]][-1],
        )
        at_user = serializer.data["at_persons"]
        if not at_user:
            # 如果@相关人没有值，发钉钉消息时，不@任何人
            bug_push_robot.send_text_msg(access_token=BUG_ROBOT["access_token"], secret=BUG_ROBOT["secret"], at_user="asdfghjkqwertyxcvbn1234567", msg=msg)
        else:
            # 如果@相关人有值，发钉钉消息时，就@这个人
            bug_push_robot.send_text_msg(access_token=BUG_ROBOT["access_token"], secret=BUG_ROBOT["secret"], at_user=at_user, msg=msg)

        return res or Response({"code": return_code.SUCCESS, "msg": "发送消息成功", "data": serializer.data})



