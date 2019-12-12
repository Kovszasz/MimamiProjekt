
from rest_framework import pagination
from rest_framework.response import Response
class CommentPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 200
    last_page_strings = ('the_end',)

#class PostPagination(pagination.PageNumberPagination):
#    page_size = 1
#    page_size_query_param = 'page_size'
#    max_page_size = 200
#    last_page_strings = ('the_end',)

class PostPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 4

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })

class TemplatePagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })
"""
class TimelinePagination(object):

    @property
    def paginator(self):

        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                 self._paginator = None
            else:
                 self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):

         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(
             queryset, self.request, view=self)

    def get_paginated_response(self, data):

         assert self.paginator is not None
         return self.paginator.get_paginated_response(data)
"""
