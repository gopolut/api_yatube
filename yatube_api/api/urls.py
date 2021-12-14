from django.db import router
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentViewSet, GroupViewSet, PostsViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/users', UserViewSet)
router.register(r'api/v1/posts', PostsViewSet)
router.register(r'api/v1/groups', GroupViewSet)
router.register(
    r'api/v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
]
