from rest_framework import serializers
from django.contrib.auth.models import User

from applications.blog.models import Blog
from applications.user.serializers import UserSerializer
from applications.post.serializers import PostViewSerializer


class BlogCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    authors = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()),
                                         required=False)

    class Meta:
        model = Blog
        exclude = ['posts', 'subscribers']

    def create(self, validated_data: dict):
        authors_ids = None

        if 'authors' in validated_data.keys():
            authors_ids = validated_data.pop('authors')
        instance = Blog.objects.create(**validated_data)

        if authors_ids:
            instance.authors.set(authors_ids)

        return instance

    def update(self, instance, validated_data: dict):
        authors_ids = None

        if 'authors' in validated_data.keys():
            authors_ids = validated_data.pop('authors')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if authors_ids is not None:
            instance.authors.set(authors_ids)

        return instance


class BlogViewSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    authors = UserSerializer(many=True, read_only=True)
    posts = PostViewSerializer(many=True, read_only=True)
    subscribers = serializers.SerializerMethodField(method_name='_subscribers')

    class Meta:
        model = Blog
        fields = '__all__'

    def _subscribers(self, obj):
        return obj.subscribers.count()


class BlogPostSerializer(serializers.ModelSerializer):
    posts = PostViewSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['posts', ]


class SubscribeBlogSerializer(serializers.ModelSerializer):
    CHOICES = (
        ('SUB', 'Subscribe'),
        ('USUB', 'Unsubscribe'),
    )
    action = serializers.ChoiceField(choices=CHOICES, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Blog
        fields = ['action', 'user']

    def update(self, instance, validated_data: dict):
        action = validated_data.get('action', None)
        user = validated_data.get('user', None)
        if action == 'SUB' and not instance.subscribers.filter(id=user.id).first():
            instance.subscribers.add(user)
        elif action == 'USUB':
            instance.subscribers.remove(user)
        instance.save()
        return instance

    def to_internal_value(self, data):
        internal_value = super(SubscribeBlogSerializer, self).to_internal_value(data)
        action = data.get("action", None)
        internal_value.update({
            "action": action
        })
        return internal_value


class AddAuthorBlogSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Blog
        fields = ['authors', ]

    def update(self, instance, validated_data):
        author = validated_data.get('authors', None)
        if author and not instance.authors.filter(id=author.id):
            instance.authors.add(author)
        return instance
