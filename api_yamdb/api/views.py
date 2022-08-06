from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, filters

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Review, Comment, Title, Category, Genre

from .filters import TitleFilter

from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
)
from .permissions import (
    IsModerOrAdminOrAuthor,
    AdminOrReadOnly,
    AdminAuthorModeratorOrReadOnly,
)


class CreateDestroyListMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (AdminAuthorModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        if self.action == "update":
            return (IsModerOrAdminOrAuthor(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (AdminAuthorModeratorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(title=title, review=review, author=self.request.user)

    def get_permissions(self):
        if self.action == "update" or self.action == "delete":
            return (IsModerOrAdminOrAuthor(),)
        return super().get_permissions()


class CategoryViewSet(CreateDestroyListMixin):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CreateDestroyListMixin):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleSerializerWrite
        return TitleSerializerRead
