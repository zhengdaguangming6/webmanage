from django.urls import path
from rest_framework import routers
from apps.user.views import account

router = routers.SimpleRouter()

# 其他注册方式
# router.register(r'comment', comment.CommentView)

urlpatterns = [
    path('auth/', account.AuthView.as_view()),
    path('test/', account.TestView.as_view()),
]