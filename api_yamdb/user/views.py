from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import User
from .pagination import UsersPagination
from .permissions import IsAdmin
from .serializers import (
    UserRegistrSerializer,
    LoginSerializer,
    UsersSerializer,
    UserNameSerializer,
    UsersListSerializer,
    UserMeSerializer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework import filters


class RegistrUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = LoginSerializer


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdmin,
    )
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=username",)
    pagination_class = UsersPagination
    lookup_field = "username"

    def get_serializer_class(self):
        if self.action == "list":
            return UsersListSerializer
        if self.action == "create":
            return UsersListSerializer
        if (self.kwargs["username"] == "me") and (
            self.action == ("partial_update" or "update")
        ):
            return UserMeSerializer
        if self.kwargs["username"]:
            return UserNameSerializer
        else:
            return UsersSerializer

    def get_permissions(self, *args, **kwargs):
        if self.kwargs:
            if self.kwargs["username"] == "me":
                return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_object(self):
        if self.kwargs["username"] == "me":
            return self.request.user
        return get_object_or_404(User, username=self.kwargs["username"])

    def destroy(self, request, *args, **kwargs):
        if self.kwargs:
            if self.kwargs["username"] == "me":
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
