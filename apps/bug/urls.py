from django.urls import path
from rest_framework import routers
from apps.bug.views import bug_list

router = routers.SimpleRouter()

# bug列表增删改查
router.register(r'bug_list', bug_list.BugView)
# bug发送钉钉消息相关
router.register(r'bug_push_message', bug_list.BugPushMessageView)

urlpatterns = []

urlpatterns += router.urls