from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Follow, Like, Post
from .serializers import CommentSerializer, PostSerializer, ProfileSerializer, RegisterSerializer

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related("likes", "comments__author")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        ids = Follow.objects.filter(follower=self.request.user).values_list("following_id", flat=True)
        return Post.objects.filter(author_id__in=ids).select_related("author").prefetch_related("likes", "comments__author")


class FollowToggleAPIView(APIView):
    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return Response({"detail": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)
        relation, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            relation.delete()
        return Response({"following": created})


class LikeToggleAPIView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return Response({"liked": created, "likes_count": post.likes.count()})
