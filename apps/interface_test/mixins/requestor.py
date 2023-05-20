import json
import requests
from rest_framework import mixins
from rest_framework.response import Response
from common import return_code
from apps.interface_test.utils.requestor import Request
from apps.interface_test.utils.assertor import Assert
from apps.interface_test.interface_config.env_config import APP_ENV, BACKSTAGE_ENV, METHOD_PARAMS


class RequestorRetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    单个接口测试
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data_dict = dict(serializer.data)
        print("data_dict============", data_dict)
        if data_dict["run"] == 0:
            return Response({"code": return_code.SUCCESS, "msg": "本接口的状态：不执行"})

        req = Request()
        phone = data_dict["phone"]
        password = data_dict["password"]
        url1 = 'https://yapi.haohaozhu.cn/Login/Login'
        data1 = {"phone": phone, "password": password, "type": "phone"}
        req_login = req(method="POST", url=url1, data=data1)
        if not req_login:
            return Response({"code": return_code.SUCCESS, "msg": "当前登录接口没有返回值，请检查请求参数", "data": req_login})
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
            return Response({"code": return_code.SUCCESS, "msg": "获取token当前登录接口失败，请检查请求参数", "data": req_login})
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
            return Response({"code": return_code.SUCCESS, "msg": "当前测试的接口报错，没有数据返回", "data": res})
        result = res.json()
        print("result7777&&&********", type(result), result)
        asserts = data_dict["asserts"]
        # <class 'str'> code=1, data.user_info.nick=张三,data.list[3].title=春天来了
        #  code=1,data.is_over=0,data.list.0.child.list.0.user_info.nick=约克小夏，data.list.0.child.list.0.user_info.uid=3240262
        print("assert==============", type(asserts), asserts)
        if not asserts:  # 没有填写断言的情况
            return Response({"code": return_code.SUCCESS, "msg": "无断言，接口测试成功", "data": result})
        if asserts: # 有断言的情况，验证断言是否通过
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
                        return Response({"code": return_code.SUCCESS, "msg": "接口测试不通过".format(k, v), "assert_code": 0, "assertion_list": assertion_list, "data": result})
                    except Exception as e:
                        print(e)
                        assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                        return Response({"code": return_code.SUCCESS, "msg": "接口测试不通过".format(k, v), "assert_code": 0, "assertion_list": assertion_list, "data": result})
                    assertion_dict = Assert().assert_two_args(response_k, val)
                    assertion_dict["asserts"] = k + "=" + v
                    assertion_list.append(assertion_dict)
                    if assertion_dict["msg"] == "不通过":
                        return Response({"code": return_code.SUCCESS, "msg": "接口测试不通过", "assert_code": 0, "assertion_list": assertion_list, "data": result})
                    print("继续多个===============")
                if len(k_list) > 1:
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
                        return Response({"code": return_code.SUCCESS, "msg": "接口测试不通过".format(k, v), "assert_code": 0, "assertion_list": assertion_list, "data": result})
                    except Exception as e:
                        print(e)
                        assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                        return Response({"code": return_code.SUCCESS, "msg": "接口测试不通过".format(k, v), "assert_code": 0, "assertion_list": assertion_list, "data": result})
                    print("val_many-----------", type(val_many), val_many)
                    print("val-----------", type(val), val)

                    assertion_dict_many = Assert().assert_two_args(val_many, val)  # 断言
                    assertion_dict_many["asserts"] = k + "=" + v
                    assertion_list.append(assertion_dict_many)
                    if assertion_dict_many["msg"] == "不通过":
                        return Response({"code": return_code.SUCCESS, "msg": "接口测试不通过", "assert_code": 0, "assertion_list": assertion_list, "data": result})
            return Response({"code": return_code.SUCCESS, "msg": "接口测试通过", "assert_code": 1, "assertion_list": assertion_list, "data": result})


class RequestorCreateModelMixin(mixins.CreateModelMixin):

    def requestor_test_all_domain(self, data_list, task_env, pro_title):
        """
        按照域名划分批量测试方法
        """

        req = Request()
        result_list = []
        for data_dict in data_list:
            if data_dict["run"] == 0 or data_dict["status"] == 0:
                # 过滤掉执行状态为0和已经被删除的接口
                continue
            if pro_title != data_dict["domain"] and pro_title != "all":
                # 过滤掉不是对应域名的接口
                continue
            print("data_dict==========================", type(data_dict), data_dict)
            print("data_dict['domain']=====================")
            print(data_dict["domain"])
            phone = data_dict["phone"]
            password = data_dict["password"]
            # url1 = 'https://yapi.haohaozhu.cn/Login/Login'
            if task_env.startswith("qa"):
                url_login = APP_ENV["yapi"]["qa_domain"] + "/Login/Login"
            elif task_env.startswith("gray"):
                url_login = APP_ENV["yapi"]["gray_domain"] + "/Login/Login"
            elif task_env.startswith("online"):
                url_login = APP_ENV["yapi"]["online_domain"] + "/Login/Login"

            data_login = {"phone": phone, "password": password, "type": "phone"}
            req_login = req(method="POST", url=url_login, data=data_login)
            try:
                req_login = req(method="POST", url=url_login, data=data_login)
                print("req_login==============")
                print(req_login)
            except Exception as e:
                res_login = {"interface_title": data_dict.get("interface_title"),
                             "path": data_dict.get("path"),
                             "msg": "当前登录接口报错",
                             "assert_code": 0,
                             "domain": data_dict["domain"],
                             "assertion_list": []}
                result_list.append(res_login)
                continue
            #     continue
            # if req_login.startswith("请求失败"):
            #     res_login = {"interface_title": data_dict.get("interface_title"),
            #                  "path": data_dict.get("path"),
            #                  "msg": "当前登录接口请求报错，错误信息：{}".format(req_login),
            #                  "assert_code": 0,
            #                  "domain": data_dict["domain"],
            #                  "assertion_list": []}
            #     result_list.append(res_login)
            #     break
            if not req_login:
                res_login = {"interface_title": data_dict.get("interface_title"),
                             "path": data_dict.get("path"),
                             "msg": "当前登录接口没有返回值，请检查请求参数",
                             "assert_code": 0,
                             "domain": data_dict["domain"],
                             "assertion_list": []}
                result_list.append(res_login)
                continue

            # 获取hhztoken
            try:
                req_login_json = req_login.json()
                hhz_token = req_login_json["data"]["hhz_token"]
                visitor_token = req_login_json["data"]["visitor_token"]
                # uid = req_login_json["data"]["uid"]
                headers = {
                    "cookie": "hhz_token={};visitor_token={}".format(hhz_token, visitor_token)
                }
                print("hhz_token===========", hhz_token)
            except Exception as e:
                res_token = {"interface_title": data_dict.get("interface_title"),
                             "path": data_dict.get("path"),
                             "msg": "获取token当前登录接口失败，请检查请求参数",
                             "assert_code": 0,
                             "domain": data_dict["domain"],
                             "assertion_list": []}
                result_list.append(res_token)
                continue
            if pro_title == data_dict["domain"]:
                if task_env.startswith("qa"):
                    url = APP_ENV[data_dict["domain"]]["qa_domain"] + data_dict["path"]
                elif task_env.startswith("gray"):
                    url = APP_ENV[data_dict["domain"]]["gray_domain"] + data_dict["path"]
                elif task_env.startswith("online"):
                    url = APP_ENV[data_dict["domain"]]["online_domain"] + data_dict["path"]
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
                    print("else=============================")
                    print(data_dict["method"])
                    print("url=============", url)
                    print("headers", type(headers), headers)
                    res = req(method=data_dict["method"], url=url, headers=headers)
                print("url=================", type(url))
                print(url)
                print("res======================", type(res))
                print(res)
                print(res.text)
                print(res.content)
                if res.startswith("请求失败"):
                    res_error = {"interface_title": data_dict.get("interface_title"),
                                 "path": data_dict.get("path"),
                                 "msg": "当前接口请求报错，错误信息：{}".format(res),
                                 "assert_code": 0,
                                 "domain": data_dict["domain"],
                                 "assertion_list": []}
                    result_list.append(res_error)
                    break
                if not res:
                    print("res=================", type(res), res)
                    res_major = {"interface_title": data_dict.get("interface_title"),
                                 "path": data_dict.get("path"),
                                 "msg": "当前测试的接口报错",
                                 "assert_code": 0,
                                 "url": url,
                                 "domain": data_dict["domain"],
                                 "assertion_list": []}
                    result_list.append(res_major)
                    continue
                try:
                    result = res.json()
                    print("result================================", type(result))
                    print(result)
                except Exception as e:
                    print("e===========================")
                    print(e)
                    res_json = {"interface_title": data_dict.get("interface_title"),
                                "path": data_dict.get("path"),
                                "msg": "当前测试的接口报错res_json",
                                "assert_code": 0,
                                "domain": data_dict["domain"],
                                "assertion_list": []}
                    result_list.append(res_json)
                    continue
                asserts = data_dict["asserts"]
                # <class 'str'> code=1, data.user_info.nick=张三,data.list[3].title=春天来了
                #  code=1,data.is_over=0,data.list.0.child.list.0.user_info.nick=约克小夏，data.list.0.child.list.0.user_info.uid=3240262
                print("assert==============", type(asserts), asserts)
                if not asserts:  # 没有填写断言的情况
                    res_no_asserts = {"interface_title": data_dict.get("interface_title"),
                                      "path": data_dict.get("path"),
                                      "msg": "没有填写断言，接口测试成功",
                                      "assert_code": 0,
                                      "domain": data_dict["domain"],
                                      "assertion_list": []}
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
                                res_asserts = {"interface_title": data_dict.get("interface_title"),
                                               "path": data_dict.get("path"),
                                               "msg": "接口测试不通过".format(k, v),
                                               "assert_code": 0,
                                               "assertion_list": assertion_list,
                                               "domain": data_dict["domain"]}
                                result_list.append(res_asserts)
                                continue
                            except Exception as e:
                                print(e)
                                assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                                res_e = {"interface_title": data_dict.get("interface_title"),
                                         "path": data_dict.get("path"),
                                         "msg": "接口测试不通过".format(k, v),
                                         "assert_code": 0,
                                         "assertion_list": assertion_list,
                                         "domain": data_dict["domain"]}
                                result_list.append(res_e)
                                continue

                            assertion_dict = Assert().assert_two_args(response_k, val)
                            assertion_dict["asserts"] = k + "=" + v
                            assertion_list.append(assertion_dict)

                            if assertion_dict["msg"] == "不通过":
                                res_single = {"interface_title": data_dict.get("interface_title"),
                                              "path": data_dict.get("path"),
                                              "msg": "接口测试不通过",
                                              "assert_code": 0,
                                              "assertion_list": assertion_list,
                                              "domain": data_dict["domain"]}
                                result_list.append(res_single)
                                continue
                            res_single_pass = {"interface_title": data_dict.get("interface_title"),
                                               "path": data_dict.get("path"),
                                               "msg": "接口测试通过",
                                               "assert_code": 1,
                                               "assertion_list": assertion_list,
                                               "domain": data_dict["domain"]}
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
                                res_k = {"interface_title": data_dict.get("interface_title"),
                                         "path": data_dict.get("path"),
                                         "msg": "接口测试不通过".format(k, v),
                                         "assert_code": 0,
                                         "assertion_list": assertion_list,
                                         "domain": data_dict["domain"]}
                                result_list.append(res_k)
                                continue
                            except Exception as e:
                                print(e)
                                assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                                res_e = {"interface_title": data_dict.get("interface_title"),
                                         "path": data_dict.get("path"),
                                         "msg": "接口测试不通过".format(k, v),
                                         "assert_code": 0,
                                         "assertion_list": assertion_list,
                                         "domain": data_dict["domain"]}
                                result_list.append(res_e)
                                continue
                            print("val_many-----------", type(val_many), val_many)
                            print("val-----------", type(val), val)

                            assertion_dict_many = Assert().assert_two_args(val_many, val)  # 断言
                            assertion_dict_many["asserts"] = k + "=" + v
                            assertion_list.append(assertion_dict_many)
                            if assertion_dict_many["msg"] == "不通过":
                                res_many = {"interface_title": data_dict.get("interface_title"),
                                            "path": data_dict.get("path"),
                                            "msg": "接口测试不通过",
                                            "assert_code": 0,
                                            "assertion_list": assertion_list,
                                            "domain": data_dict["domain"]}
                                result_list.append(res_many)
                                continue
            elif pro_title == "all":
                for pro in APP_ENV:
                    if pro == data_dict["domain"]:
                        if task_env.startswith("qa"):
                            url = APP_ENV[data_dict["domain"]]["qa_domain"] + data_dict["path"]
                        if task_env.startswith("gray"):
                            url = APP_ENV[data_dict["domain"]]["gray_domain"] + data_dict["path"]
                        if task_env.startswith("online"):
                            url = APP_ENV[data_dict["domain"]]["online_domain"] + data_dict["path"]
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
                            print("else=============================")
                            print(data_dict["method"])
                            print("url=============", url)
                            print("headers", type(headers), headers)
                            res = req(method=data_dict["method"], url=url, headers=headers)
                        print("url=================", type(url))
                        print(url)

                        if not res:
                            print("res=================", type(res), res)
                            res_major = {"interface_title": data_dict.get("interface_title"),
                                         "path": data_dict.get("path"),
                                         "msg": "当前测试的接口报错",
                                         "url": url,
                                         "assert_code": 0,
                                         "domain": pro,
                                         "assertion_list": []}
                            result_list.append(res_major)
                            continue
                        try:
                            result = res.json()
                            print("result================================", type(result))
                            # print(result)
                        except Exception as e:
                            print("e===========================")
                            print(e)
                            res_json = {"interface_title": data_dict.get("interface_title"),
                                        "path": data_dict.get("path"),
                                        "msg": "当前测试的接口报错res_json",
                                        "assert_code": 0,
                                        "domain": pro,
                                        "assertion_list": []}
                            result_list.append(res_json)
                            continue
                        asserts = data_dict["asserts"]
                        # <class 'str'> code=1, data.user_info.nick=张三,data.list[3].title=春天来了
                        #  code=1,data.is_over=0,data.list.0.child.list.0.user_info.nick=约克小夏，data.list.0.child.list.0.user_info.uid=3240262
                        print("assert==============", type(asserts), asserts)
                        if not asserts:  # 没有填写断言的情况
                            res_no_asserts = {"interface_title": data_dict.get("interface_title"),
                                              "path": data_dict.get("path"),
                                              "msg": "没有填写断言，接口测试成功",
                                              "assert_code": 0,
                                              "domain": pro,
                                              "assertion_list": []}
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
                                        res_asserts = {"interface_title": data_dict.get("interface_title"),
                                                       "path": data_dict.get("path"),
                                                       "msg": "接口测试不通过".format(k, v),
                                                       "assert_code": 0,
                                                       "assertion_list": assertion_list,
                                                       "domain": pro}
                                        result_list.append(res_asserts)
                                        break
                                    except Exception as e:
                                        print(e)
                                        assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                                        res_e = {"interface_title": data_dict.get("interface_title"),
                                                 "path": data_dict.get("path"),
                                                 "msg": "接口测试不通过".format(k, v),
                                                 "assert_code": 0,
                                                 "assertion_list": assertion_list,
                                                 "domain": pro}
                                        result_list.append(res_e)
                                        break

                                    assertion_dict = Assert().assert_two_args(response_k, val)
                                    assertion_dict["asserts"] = k + "=" + v
                                    assertion_list.append(assertion_dict)

                                    if assertion_dict["msg"] == "不通过":
                                        res_single = {"interface_title": data_dict.get("interface_title"),
                                                      "path": data_dict.get("path"),
                                                      "msg": "接口测试不通过",
                                                      "assert_code": 0,
                                                      "assertion_list": assertion_list,
                                                      "domain": pro}
                                        result_list.append(res_single)

                                    else:
                                        res_single_pass = {"interface_title": data_dict.get("interface_title"),
                                                           "path": data_dict.get("path"),
                                                           "msg": "接口测试通过",
                                                           "assert_code": 1,
                                                           "assertion_list": assertion_list,
                                                           "domain": pro}
                                        result_list.append(res_single_pass)
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
                                    except Exception as e:
                                        print(e)
                                        assertion_list.append({"error": "{}={} 错误，没找到{},请检查".format(k, v, k)})
                                        res_e = {"interface_title": data_dict.get("interface_title"),
                                                 "path": data_dict.get("path"),
                                                 "msg": "接口测试不通过".format(k, v),
                                                 "assert_code": 0,
                                                 "assertion_list": assertion_list,
                                                 "domain": pro}
                                        result_list.append(res_e)
                                        break
                                    print("val_many-----------", type(val_many), val_many)
                                    print("val-----------", type(val), val)

                                    assertion_dict_many = Assert().assert_two_args(val_many, val)  # 断言
                                    assertion_dict_many["asserts"] = k + "=" + v
                                    assertion_list.append(assertion_dict_many)
                                    if assertion_dict_many["msg"] == "不通过":
                                        res_many = {"interface_title": data_dict.get("interface_title"),
                                                    "path": data_dict.get("path"),
                                                    "msg": "接口测试不通过",
                                                    "assert_code": 0,
                                                    "assertion_list": assertion_list,
                                                    "domain": pro}
                                        result_list.append(res_many)
                                        break
                                    else:
                                        res_many = {"interface_title": data_dict.get("interface_title"),
                                                    "path": data_dict.get("path"),
                                                    "msg": "接口测试通过",
                                                    "assert_code": 1,
                                                    "assertion_list": assertion_list,
                                                    "domain": pro}
                                        result_list.append(res_many)

        return result_list


    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()     # 获取数据表的所有数据
        data_list = list(queryset.values())
        print("data_list=========", type(data_list), data_list)

        receive_data = request.data    # 获取前端提交的数据
        # <class 'dict'> {'task_title': '测试任务1', 'task_env': 'qa23', 'pro_title': 'tapi'}
        print("receive_data::::::", type(receive_data), receive_data)
        task_title = receive_data["task_title"]
        task_env = receive_data["task_env"]
        pro_title = receive_data["pro_title"]

        """
        if pro_title == "all":
            url_list = []
            for k in APP_ENV.keys():
                pro = APP_ENV.get(k)
                if task_env.startswith("qa"):
                    env = pro["test_domain"].format(id=task_env)
                    print("env=======", env)
                    url_list.append(env)
                elif task_env.startswith("gray"):
                    env = pro["gray_domain"].format(id=task_env)
                    print("env=======", env)
                    url_list.append(env)
                elif task_env.startswith("online"):
                    env = pro["online_domain"]
                    print("env=======", env)
                    url_list.append(env)
            print("url_list=======", url_list)

        else:
            pro = APP_ENV.get(pro_title)
            print("pro========", type(pro), pro)
            if task_env.startswith("qa"):
                env = pro["test_domain"].format(id=task_env)
                print("env=======", env)
            elif task_env.startswith("gray"):
                env = pro["gray_domain"].format(id=task_env)
                print("env=======", env)
            elif task_env.startswith("online"):
                env = pro["online_domain"]
                print("env=======", env)
        """

        res_list = self.requestor_test_all_domain(data_list=data_list, task_env=task_env, pro_title=pro_title)
        res_list_str = json.dumps(res_list)
        data_res = {
            "task_title": task_title,
            "task_env": task_env,
            "pro_title": pro_title,
            "content": res_list_str,
            "status": 1
        }
        serializer = self.get_serializer(data=data_res)
        print("serializer接口记录------", type(serializer), serializer)
        # 1.异常处理
        if not serializer.is_valid():
            result = {"code": return_code.VALIDATE_ERROR, "detail": serializer.errors, "msg": "保存失败,请检查传参"}
            return Response(result)

        # 2.优化perform_create保存数据
        res = self.perform_create(serializer)
        # 3.返回数据的处理
        return Response({"code": return_code.SUCCESS, "msg": "接口测试完成"})


class RequestorReportPrimaryListModelMixin(mixins.ListModelMixin):
    """查询多条测试报告列表"""
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({"code": return_code.SUCCESS, "data": serializer.data})


class RequestorReportPrimaryRetrieveModelMixin(mixins.RetrieveModelMixin):
    """查询单条测试报告的详细数据"""
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class_retrieve(instance)
        return Response({"code": return_code.SUCCESS, "msg": "查询单条测试报告数据成功", "data": serializer.data})


# 删除一条数据
class RequestorReportPrimaryDestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        res = self.perform_destroy(instance)
        return Response({"code": return_code.SUCCESS, "msg": "删除成功"})