from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied # MethodNotAllowed, AuthenticationFailed

from rest_framework.permissions import IsAuthenticated

from posts.models import User, Post, Group
from .serializers import CommentSerializer, UserSerializer, PostSerializer, GroupsSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):   
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Запрет на изменение чужого контента
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostsViewSet, self).perform_update(serializer)
    
    # Запрет на удаление чужого контента
    def perform_destroy(self, instance):
            if instance.author != self.request.user:
                raise PermissionDenied('Удаление чужого контента запрещено!')
            return super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
 

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    

    def get_queryset(self):       
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        print('user: ', self.request.user)
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

    # Запрет на изменение чужого контента
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено')
        super().perform_update(serializer)
    
    # Запрет на удаление чужого контента
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        return super().perform_destroy(instance)
