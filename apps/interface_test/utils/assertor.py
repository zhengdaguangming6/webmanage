#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Assert(object):

    def assert_two_args(self, k, v):
        # 比较两个值是否相等
        if not k == v:
            assertion = "{}=={}".format(k, v)
            assertion_dict = {"msg": "不通过", "assertion": assertion}
            return assertion_dict
        else:
            assertion = "{}=={}".format(k, v)
            assertion_dict = {"msg": "通过", "assertion": assertion}
            return assertion_dict

    def str_to_obj(self, k_list, res_str):
        """
        list1 = ["data", "is_over"]
        把list1列表中的断言的键，变为 result["data"]["is_over"]
        return: 返回result字典对应的值
        如果列表list1有数字，例如 ["data", "0"， "is_over"]，会把字符串"0"变为int 0
        """
        val = ""
        for i in k_list:
            if i.isdecimal():
                val += "[{}]".format(i)
                print(type(val), val)
            else:
                val += "['{}']".format(i)
        v = res_str + val
        print(v, type(v))
        return eval(v)


if __name__ == "__main__":
    # result = {"data":
    #               {"is_over": 0}
    #           }
    result = {"data":[
                  {"is_over": 0}
                ]
              }
    data_list = ['data', '0', 'is_over']
    a = Assert().str_to_obj(data_list, "result")
    print(a, type(a))