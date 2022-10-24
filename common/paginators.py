from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomResultsSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                {
                    "ok": True,
                    "data": {
                        "count": self.page.paginator.count,
                        "next": self.get_next_link(),
                        "previous": self.get_previous_link(),
                        "results": data,
                    },
                }
            )
        )
