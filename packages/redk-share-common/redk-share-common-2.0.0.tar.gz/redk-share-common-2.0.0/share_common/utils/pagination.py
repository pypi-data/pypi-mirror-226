from rest_framework.pagination import OrderedDict, PageNumberPagination
from rest_framework.response import Response


class RedkernelPagination(PageNumberPagination):
    page_size_query_param = "pageSize"
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link() if self.get_next_link() else ""),
                    (
                        "previous",
                        self.get_previous_link() if self.get_previous_link() else "",
                    ),
                    ("results", data),
                ]
            )
        )
