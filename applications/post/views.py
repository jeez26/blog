from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from applications.post.models import Post
from applications.post.serializers import PostCreateSerializer, PostViewSerializer, LikePostSerializer, \
    CommentPostSerializer
from permissions.permissions import IsAutorOrAdminOrReadOnly, CreatePostPermission


class PostListAPIView(ListAPIView):
    queryset = Post.objects.order_by("created_at")
    serializer_class = PostViewSerializer
    permission_classes = [IsAuthenticated]


class MyPostAPIView(ListAPIView):
    queryset = Post.objects.order_by("created_at")
    serializer_class = PostViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class PostViewAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAutorOrAdminOrReadOnly]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostViewSerializer
        return PostCreateSerializer

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get(self.lookup_field, None))
        post.views += 1
        post.save()
        return super().get(request, *args, **kwargs)


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [CreatePostPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={
            'blog_id': kwargs.get('blog_id', None),
            'request': request
        })

        if serializer.is_valid():
            post = serializer.create(validated_data=serializer.validated_data)
            return Response(data="Ok!", status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePostAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class CommentPostAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
