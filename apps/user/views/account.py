from rest_framework.views import APIView
from rest_framework.response import Response
from apps.user.serializers.account import AuthSerializer
from common import return_code
from django.conf import settings
from apps.user import models
import jwt
import datetime


class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)

        # 1.获取用户请求发送的用户名和密码

        # 2。数据校验
        serializer = AuthSerializer(data=request.data)
        print("校验后的数据serializer---------", type(serializer), serializer)
        print("serializer.is_valid()------", type(serializer.is_valid()), serializer.is_valid())
        if not serializer.is_valid():
            # {username:[用户名不能为空, ]}
            return Response({"code": return_code.FIELD_ERROR, "detail": serializer.errors})

        # 3.数据库校验
        print("serializer.validated_data------", type(serializer.validated_data), serializer.validated_data)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        if not user_object:
            return Response({"code": return_code.VALIDATE_ERROR, "detail": "用户名或密码错误"})
        user_id = user_object.id
        # 4。生成jwt token 返回
        headers = {
            'typ': 'jwt',
            'alg': "HS256"
        }
        # 构造payload
        payload = {
            'user_id': user_id,  # 用户ID
            'username': user_object.username,  # 用户名
            # 'exp': datetime.datetime.now() + datetime.timedelta(minutes=1) # 超时时间
            'exp': datetime.datetime.now() + datetime.timedelta(days=7) # 超时时间
            # 'exp': datetime.datetime.now() + datetime.timedelta(seconds=5) # 超时时间
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256", headers=headers)

        result = {
            "code": return_code.SUCCESS,
            "data": {
                "token": token,
                "username": username,
                "uid": user_id,
            }
        }

        return Response(result)


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.user.user_id)
        print(request.user.username)
        print(request.user.exp)
        print(request.auth)
        return Response("test")