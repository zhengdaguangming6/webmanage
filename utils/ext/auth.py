"""jwttoken认证功能"""

import jwt

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from common import return_code


class Current(object):
    def __init__(self, user_id, username, exp):
        self.user_id = user_id
        self.username = username
        self.exp = exp


class MyAuthenticationFailed(AuthenticationFailed):
    status_code = 200


class JwtTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 读取用提交的jwt token
        # 去请求url中获取token
        # token = request.query_params.get("token")

        # 去请求头中获取token   Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
        token = request.META.get("HTTP_AUTHORIZATION")
        print(type(token))
        print(token)
        if not token:
            # 状态码是401，内容：{code:2000, "error": "认证失败"}
            # raise AuthenticationFailed({"code": return_code.AUTH_FAILED, "error": "认证失败"})
            # 状态码是200，内容：{code:2000, "error": "认证失败"}
            raise MyAuthenticationFailed({"code": return_code.AUTH_FAILED, "error": "认证失败"})

        # jwttoken校验
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
            print(payload, type(payload))   # {'user_id': 1, 'username': '小红', 'exp': 1679721821} <class 'dict'>
            return Current(**payload), token
        except Exception as e:
            # raise AuthenticationFailed({"code": return_code.AUTH_FAILED, "error": "认证失败"})
            raise MyAuthenticationFailed({"code": return_code.AUTH_FAILED, "error": "认证失败"})
        # return xx, xxx  # request.user/request.auth
        # 抛出异常

    def authenticate_header(self, request):
        return 'Bearer realm="API"'