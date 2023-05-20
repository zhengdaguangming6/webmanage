#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.interface_test import models
from apps.user import models as user_models


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserInfo
        fields = ["id", "username"]
        read_only_fields = ["username"]


class InterfaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InterfaceTest
        fields = [
            "id", "interface_title", "phone", "username",  "password", "method", "path", "domain", "params", "data", "json",
            "headers", "asserts", "run", "status", "create_time", "update_time", "update_user", "create_user", "notes",
        ]
        read_only_fields = ["create_time", "update_time", "update_user", "create_user"]
        extra_kwargs = {
            "status": {"read_only": True},  # 序列化
            # "map_username": {"required": False},
        }


class InterfaceRetrieveSerializer(serializers.ModelSerializer):
    create_user = UserInfoSerializer(read_only=True)
    update_user = UserInfoSerializer(read_only=True)

    class Meta:
        model = models.InterfaceTest
        fields = [
            "id", "interface_title", "phone", "username",  "password", "method", "path", "domain", "params", "data", "json",
            "headers", "asserts", "run", "notes", "create_time", "update_time", "update_user", "create_user"
        ]
        read_only_fields = ["id", "interface_title", "phone", "username",  "password", "method", "path", "domain", "params", "data", "json",
            "headers", "asserts", "run", "notes", "create_time", "update_time", "update_user", "create_user"]
