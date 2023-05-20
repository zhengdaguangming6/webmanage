from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.bug import models
from apps.user import models as user_models


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserInfo
        fields = ["id", "username"]
        read_only_fields = ["username"]


class BugSerializer(serializers.ModelSerializer):
    create_user = UserInfoSerializer(read_only=True)
    update_user = UserInfoSerializer(read_only=True)

    class Meta:
        model = models.BugList
        fields = "__all__"
        read_only_fields = ["create_time", "update_time", "update_user", "create_user"]
