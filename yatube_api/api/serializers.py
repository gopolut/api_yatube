from rest_framework import serializers

from posts.models import User, Post, Group, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'comments')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
  
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created', )
        read_only_fields = ('author', 'post', 'created', )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, required=False)
    
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'group', 'image', 'pub_date', 'comments')


class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', )
