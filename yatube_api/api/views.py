from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post, User
# isort здесь добавляет пустую строку
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, GroupsSerializer, PostSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)
