from django.middleware.security import SecurityMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


# 绕过浏览器的同源策略
class CorsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "OPTIONS":
            return HttpResponse()   #如果有返回值，就不会去执行后面的中间件和视图函数，直接执行当前中间件的 process_response

    # 绕过浏览器的同源策略
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Request-Method'] = '*'
        response['Access-Control-Allow-Methods'] = '*'
        return response