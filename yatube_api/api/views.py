
from django.shortcuts import get_object_or_404
from rest_framework import  filters, permissions, viewsets, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.authtoken.views import ObtainAuthToken

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post, User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)

class GroupViewSet(viewsets.ReadOnlyModelViewSet, ObtainAuthToken):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
# class GroupViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')
    
    def get_queryset(self):
        user = self.request.user
        new_queryset = user.followers.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def validate_fallowing(self, value):
        if value == self.request.user:
            raise serializers.ValidationError('Подписака на себя не возмжна')
        return value