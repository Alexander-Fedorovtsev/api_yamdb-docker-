from rest_framework.pagination import LimitOffsetPagination


class UsersPagination(LimitOffsetPagination):
    default_limit = 100
