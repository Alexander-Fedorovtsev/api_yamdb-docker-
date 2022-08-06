from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ReviewViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from user.views import (
    RegistrUserView,
    LoginView,
    UsersViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register("users", UsersViewSet, basename="users")

urlpatterns = [
    path(
        "v1/auth/token/",
        LoginView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "v1/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("v1/auth/signup/", RegistrUserView.as_view(), name="registr"),
    path("v1/", include(router_v1.urls)),
]
