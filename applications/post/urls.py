from django.urls import path

from applications.post.views import PostListAPIView, PostViewAPIView, \
    PostCreateAPIView, LikePostAPIView, MyPostAPIView, CommentPostAPIView

urlpatterns = [
    path('list/', PostListAPIView.as_view()),
    path('blog/<int:blog_id>', PostCreateAPIView.as_view()),
    path('<int:id>', PostViewAPIView.as_view()),
    path('like/<int:id>', LikePostAPIView.as_view()),
    path('comment/<int:id>', CommentPostAPIView.as_view()),
    path('my/', MyPostAPIView.as_view()),
]
