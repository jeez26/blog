from django.urls import path

from applications.blog.views import BlogListAPIView, \
    BlogViewAPIView, BlogCreateAPIView, BlogPostsAPIView, \
    SubscribeBlogAPIView, MyBlogAPIView, AddAuthorBlogAPIView

urlpatterns = [
    path('list/', BlogListAPIView.as_view()),
    path('', BlogCreateAPIView.as_view()),
    path('<int:id>', BlogViewAPIView.as_view()),
    path('<int:id>/posts/', BlogPostsAPIView.as_view()),
    path('subsribe/<int:id>', SubscribeBlogAPIView.as_view()),
    path('add_author/<int:id>', AddAuthorBlogAPIView.as_view()),
    path('my/', MyBlogAPIView.as_view()),
]
