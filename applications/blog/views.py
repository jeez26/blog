from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from applications.blog.models import Blog
from applications.blog.serializers import BlogCreateSerializer, BlogViewSerializer, BlogPostSerializer, \
    SubscribeBlogSerializer, AddAuthorBlogSerializer
from permissions.permissions import IsOwnerOrIsAdminOrReadOnly
from rest_framework.filters import OrderingFilter
from django.db.models import Count, F


class BlogListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogViewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'authors__username']
    ordering_fields = ['title', 'created_at', 'updated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', [])

        if ordering.find('relevant') != -1:
            queryset = queryset.annotate(
                num_authors=Count('authors'),
                num_posts=Count('posts'),
                relevant=F('num_posts') + F('num_authors') * 0.5
            )

        return queryset.order_by(ordering if ordering else 'updated_at')


class MyBlogAPIView(ListAPIView):
    queryset = Blog.objects.order_by("created_at")
    serializer_class = BlogViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(subscribers=self.request.user)


class BlogPostsAPIView(ListAPIView):
    queryset = Blog.objects.order_by("updated_at")
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'id' in self.kwargs.keys():
            blog_id = self.kwargs.get('id', None)
            return Blog.objects.filter(id=blog_id).order_by("updated_at")
        return super().get_queryset()


class BlogViewAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsOwnerOrIsAdminOrReadOnly]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogViewSerializer
        return BlogCreateSerializer



class BlogCreateAPIView(CreateAPIView):
    serializer_class = BlogCreateSerializer
    permission_classes = [IsAuthenticated]


class SubscribeBlogAPIView(UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = SubscribeBlogSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class AddAuthorBlogAPIView(UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = AddAuthorBlogSerializer
    permission_classes = [IsOwnerOrIsAdminOrReadOnly]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = Blog.objects.filter(id=kwargs.get("id", None)).first()
            serializer.update(instance, serializer.validated_data)
            return Response(data="Ok!", status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

