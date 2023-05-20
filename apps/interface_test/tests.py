from django.test import TestCase

# Create your tests here.

# a = {"name": "张三", "age": 24}
# b = str(a)
#
# print(b, type(b))

# import json
# # a = '{"name": "张三", "age": 24}'
# a = '{"room_id": "812"}'
# b = json.loads(a)
# #
# print(b, type(b))

# a = bool("")
# print(a, type(a))
#
# a = {"name": "张三", "age": 18}
# print(a.keys(), type(a.keys()), len(a.keys()))

# from django.db import models
# from apps.user.models import UserInfo
#
#
# class InterfaceTest(models.Model):
#
#     create_user = models.ForeignKey(verbose_name="创建人uid", to=UserInfo, to_field="id", on_delete=models.DO_NOTHING)
#     update_uid = models.ForeignKey(verbose_name="更新人uid", to=UserInfo, to_field="id", null=True, default=0, on_delete=models.DO_NOTHING)
# try:
#     assert 1 == 2
# except Exception as e:
#     print(e)


# def add(a, **kwargs):
#     print(kwargs)
#     return kwargs
#
#
# b = add(1, **{"name": "张三", "age": 18})
# print(b)

# a = ''
# b = None
# print(id(a))
# print(id(b))
# if a is None:
#     print("a这是None")
#
# if b is None:
#     print("b这是None")

# a = "34"
# print(a.isdecimal())


# a = ['data', '0', 'is_over']
#
# result = {"data":
#               [
#                   {"is_over": 0}
#               ]
#           }
#
# c = ""
# for i in a:
#     if i.isdecimal():
#         c += "[{}]".format(i)
#     else:
#         c += "['{}']".format(i)
#
# print(c, type(c))
# d = "result" + c
# print(d, type(d))
# res = eval(d)
# print(res, type(res))

import json

# a = "{'page': '1'}"
a = '{"page": "1"}'

b = json.loads(a)
print(type(b), b)