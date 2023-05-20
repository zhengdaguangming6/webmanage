from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from apps.interface_test import models
from apps.interface_test.mixins.requestor import RequestorRetrieveModelMixin, RequestorCreateModelMixin, RequestorReportPrimaryListModelMixin, RequestorReportPrimaryRetrieveModelMixin, RequestorReportPrimaryDestroyModelMixin
from apps.interface_test.serializers.requestor import RequestorSerializer, RequestorReportPrimarySerializer, RequestorReportPrimaryRetrieveSerializer
from apps.interface_test.serializers.interface import InterfaceSerializer
from rest_framework.response import Response
from common import return_code
from apps.interface_test.utils.requestor import Request
from apps.interface_test.interface_config.env_config import APP_ENV
from apps.interface_test.utils.assertor import Assert
from apps.interface_test.extension.page import RequestorReportPrimaryPageNumberPagination




class RequestorView(RequestorRetrieveModelMixin, RequestorCreateModelMixin, GenericViewSet):
    """
    单接口测试retrieve
    区分域名接口自动化测试 create
    """
    queryset = models.InterfaceTest.objects.filter(status=1).order_by("-id")
    serializer_class = InterfaceSerializer

    # 把post请求的传参保存到数据库
    def perform_create(self, serializer):
        # 保存创建人的uid
        serializer.save(create_user_id=self.request.user.user_id)
        result = {"code": return_code.SUCCESS, "msg": "保存成功", "data": serializer.data}
        return Response(result)


    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        if self.request.method == "POST":
            return RequestorSerializer


        return self.serializer_class


class RequestorManyView(APIView):
    """
    批量测试
    """
    def post(self, request, *args, **kwargs):
        receive_data = request.data
        print("receive_data", type(receive_data), receive_data)
        data_list = receive_data["data_list"]
        print("data_list=============", type(data_list), data_list)
        result_list = []

        for i in data_list:
            data_dict = i
            print("data_dict============", data_dict)
            if data_dict["run"] == 0:
                res_dict = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"), "msg": "当前接口不执行"}
                result_list.append(res_dict)
                continue
            req = Request()
            phone = data_dict["phone"]
            password = data_dict["password"]
            url1 = 'https://yapi.haohaozhu.cn/Login/Login'
            data1 = {"phone": phone, "password": password, "type": "phone"}
            req_login = req(method="POST", url=url1, data=data1)
            if not req_login:
                res_login = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"), "msg": "当前登录接口没有返回值，请检查请求参数"}
                result_list.append(res_login)
                continue
            req_login_json = req_login.json()
            # 获取hhztoken
            try:
                hhz_token = req_login_json["data"]["hhz_token"]
                # visitor_token = req_login_json["data"]["visitor_token"]
                # uid = req_login_json["data"]["uid"]
                headers = {
                    "cookie": "hhz_token={}".format(hhz_token),
                }
                print("hhz_token===========", hhz_token)
            except Exception as e:
                res_token = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                             "msg": "获取token当前登录接口失败，请检查请求参数", "assert_code": 0}
                result_list.append(res_token)
                continue
            # 线上环境
            url = APP_ENV[data_dict["domain"]]["online_domain"] + data_dict["path"]
            print("线上URL", url)
            if data_dict["params"]:
                print("params=============", data_dict["params"])
                params = eval(data_dict["params"])
                res = req(method=data_dict["method"], url=url, params=params, headers=headers)
            elif data_dict["json"]:
                json_d = eval(data_dict["json"])
                print("json_d", type(json_d), json_d)
                res = req(method=data_dict["method"], url=url, json=json_d, headers=headers)
            elif data_dict["data"]:
                data = eval(data_dict["data"])
                res = req(method=data_dict["method"], url=url, data=data, headers=headers)
            else:
                res = req(method=data_dict["method"], url=url, headers=headers)
            if not res:
                res_major = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                             "msg": "当前测试的接口报错"}
                result_list.append(res_major)
                continue
            result = res.json()
            print("result7777&&&********", type(result), result)
            asserts = data_dict["asserts"]
            # <class 'str'> code=1, data.user_info.nick=张三,data.list[3].title=春天来了
            #  code=1,data.is_over=0,data.list.0.child.list.0.user_info.nick=约克小夏，data.list.0.child.list.0.user_info.uid=3240262
            print("assert==============", type(asserts), asserts)
            if not asserts:  # 没有填写断言的情况
                res_no_asserts = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                             "msg": "无断言，接口测试成功", "assert_code": 1}
                result_list.append(res_no_asserts)
                continue
            if asserts:  # 有断言的情况，验证断言是否通过
                assertion_list = []
                asserts_list = asserts.strip().split(",")
                # ['code=1', ' data.user_info.nick=张三', 'data.list[3].title=春天来了']
                # ['code=1', 'data.is_over=0', 'data.list.0.child.list.0.user_info.nick=约克小夏
                # data.list.0.child.list.0.user_info.uid=3240262']
                print(asserts_list)
                for i in asserts_list:
                    k, v = i.strip().split("=")
                    print(k, v)
                    print("v=========", type(v), v)
                    k_list = k.strip().split(".")
                    print("k_list===========", k_list)

                    if v.isdecimal():
                        val = int(v)
                    else:
                        val = v
                    if len(k_list) == 1:
                        print("len(k_list) == 1：--------", k, v)
                        print("split后 v=========", type(v), v)
                        try:
                            response_k = result[k]
                        except KeyError:
                            assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                            res_asserts = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                                              "msg": "接口测试不通过".format(k, v), "assert_code": 0, "assertion_list": assertion_list}
                            result_list.append(res_asserts)
                            continue
                        except Exception as e:
                            print(e)
                            assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                            res_e = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                                           "msg": "接口测试不通过".format(k, v), "assert_code": 0,
                                           "assertion_list": assertion_list}
                            result_list.append(res_e)
                            continue

                        assertion_dict = Assert().assert_two_args(response_k, val)
                        assertion_dict["asserts"] = k + "=" + v
                        assertion_list.append(assertion_dict)

                        if assertion_dict["msg"] == "不通过":
                            res_single = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                         "msg": "接口测试不通过", "assert_code": 0, "assertion_list": assertion_list}
                            result_list.append(res_single)
                            continue
                        res_single_pass = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                         "msg": "接口测试通过", "assert_code": 1, "assertion_list": assertion_list}
                        result_list.append(res_single_pass)
                        print("继续多个===============")
                    print("1111111111111111111")
                    if len(k_list) > 1:
                        print("222222222222222222")
                        # val_many = Assert().str_to_obj(k_list, "result")  # 获取该接口测试中，result结果中的对应的值
                        v1 = ""

                        for a in k_list:
                            if a.isdecimal():

                                v1 += "[{}]".format(a)
                                print(type(v1), v1)
                            else:
                                v1 += "['{}']".format(a)
                        v2 = "result" + v1
                        print(v2, type(v2))
                        try:
                            val_many = eval(v2)
                        except KeyError:
                            assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                            res_k = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                                          "msg": "接口测试不通过".format(k, v), "assert_code": 0, "assertion_list": assertion_list}
                            result_list.append(res_k)
                            continue
                        except Exception as e:
                            print(e)
                            assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                            res_e = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                                          "msg": "接口测试不通过".format(k, v), "assert_code": 0,
                                          "assertion_list": assertion_list}
                            result_list.append(res_e)
                            continue
                        print("val_many-----------", type(val_many), val_many)
                        print("val-----------", type(val), val)

                        assertion_dict_many = Assert().assert_two_args(val_many, val)  # 断言
                        assertion_dict_many["asserts"] = k + "=" + v
                        assertion_list.append(assertion_dict_many)
                        if assertion_dict_many["msg"] == "不通过":
                            res_many = {"接口名称": data_dict.get("interface_title"), "path": data_dict.get("path"),
                                     "msg": "接口测试不通过", "assert_code": 0,
                                     "assertion_list": assertion_list}
                            result_list.append(res_many)
                            continue

        return Response({"code": return_code.SUCCESS, "data": result_list})


class RequestorReportPrimaryView(RequestorReportPrimaryListModelMixin, RequestorReportPrimaryRetrieveModelMixin, RequestorReportPrimaryDestroyModelMixin, GenericViewSet):
    """
    外层-测试报告
    """
    queryset = models.Requestor.objects.filter(status=1).order_by("-id")
    serializer_class = RequestorReportPrimarySerializer
    pagination_class = RequestorReportPrimaryPageNumberPagination

    # 查看单条数据所用的序列化类
    serializer_class_retrieve = RequestorReportPrimaryRetrieveSerializer

    # 把某一条数据status改成0，作为逻辑删除
    def perform_destroy(self, instance):
        instance.status = 0
        instance.save()










