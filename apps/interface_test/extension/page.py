from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from common import return_code


# http://127.0.0.1:8000/api/interface_test/interface/?page=1&size=10
class InterfacePageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = "size"
    page_size = 10  # 如果不传参数，默认每页显示10条
    max_page_size = 1000  # 最多每页显示1000条

    def get_paginated_response(self, data):
        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data)
        # ]))
        res = {
            'code': return_code.SUCCESS,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }
        return Response(res)


class RequestorReportPrimaryPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = "size"
    page_size = 10  # 如果不传参数，默认每页显示10条
    max_page_size = 1000  # 最多每页显示1000条

    def get_paginated_response(self, data):
        res = {
            'code': return_code.SUCCESS,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }
        return Response(res)