import requests


class Request(object):
    """http请求工具类"""
    def __init__(self):
        # 实例化session管理器，维持会话, 跨请求的时候保存参数
        self.session = requests.session()

    def send(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """
        :param method: http请求方式
        :param url: 请求地址
        :param params: 字典或bytes，作为参数增加到url中
        :param data: data类型传参，字典、字节序列或文件对象，作为Request的内容
        :param json: json传参，作为Request的内容
        :param headers: 请求头，字典
        :param kwargs: 若还有其他的参数，使用可变参数字典形式进行传递
        :return:
        """
        # 对异常进行捕获
        try:
            response = self.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)
            # 返回响应结果
            return response

        except Exception as e:
            # 异常处理 报错在日志中打印具体信息
            error = f"请求失败：{e}"
            print(error)
            return error

    def __call__(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """当把一个对象，当成函数来使用，那么就指定执行当前对象的__call__"""
        return self.send(method, url, params=params, data=data, json=json, headers=headers, **kwargs)






# if __name__ == "__main__":
    # req = Request()
    # res = req(method="GET", url="https://tapi.haohaozhu.com/Album/DaRenAlbum", params=None, data=None, json=None, headers=None)
    # # print(res.text)
    # print(res.json())

    # a = Assert("1", "1").assert_two_args()
    # print(a)