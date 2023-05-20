from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.interface_test import models
from apps.user import models as user_models
import json


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserInfo
        fields = ["id", "username"]
        read_only_fields = ["username"]


class RequestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Requestor
        fields = [
            "id", "task_title", "task_env", "pro_title", "content", "status", "create_user", "create_time"
        ]
        read_only_fields = ["create_time", "create_user"]
        # extra_kwargs = {
        #     # "status": {"read_only": True},  # 序列化
        #     # "map_username": {"required": False},
        # }



class RequestorReportPrimarySerializer(serializers.ModelSerializer):
    create_user = UserInfoSerializer(read_only=True)

    class Meta:
        model = models.Requestor
        fields = [
            "id", "task_title", "task_env", "pro_title", "status", "create_user", "create_time"
        ]
        read_only_fields = ["create_time", "create_user"]


class RequestorReportPrimaryRetrieveSerializer(serializers.ModelSerializer):
    create_user = UserInfoSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = models.Requestor
        fields = [
            "id", "task_title", "task_env", "pro_title", "content", "status", "create_user", "create_time"
        ]
        read_only_fields = ["create_time", "create_user", "content"]

    def get_content(self, obj):
        # obj:表示当前要序列化那一行数据的对象
        data_dict = json.loads(obj.content)
        return data_dict