from rest_framework import permissions
from rest_framework.request import Request

from applications.blog.models import Blog


class IsOwnerOrIsAdminOrReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

        return obj.owner == request.user and request.method != "DELETE"


class IsAutorOrAdminOrReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

        return obj.author == request.user and request.method != "DELETE"


class CreatePostPermission(permissions.IsAuthenticated):

    def has_permission(self, request: Request, view):
        has_perm = super().has_permission(request=request, view=view)
        blog_id = view.kwargs.get("blog_id", None)
        blog = Blog.objects.filter(id=blog_id).first()
        if blog:
            return (blog.owner.id == request.user.id
                    or blog.authors.filter(id=request.user.id)) \
                and has_perm

        return False
