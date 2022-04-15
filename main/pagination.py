from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        try:
            self.title = kwargs['title']
        except KeyError:
            self.title = 'Заголовок станицы'
        super().__init__(*args, **kwargs)


    def get_paginated_response(self, data):
            return Response({
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'title': self.title,
                'results': data,
            })
