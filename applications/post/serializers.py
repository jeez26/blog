from rest_framework import serializers

from applications.blog.models import Blog
from applications.post.models import Post, Tag, Comment
from applications.user.serializers import UserSerializer, SmallUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = SmallUserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    body = serializers.CharField(required=False)
    tags = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all()),
                                      required=False)

    class Meta:
        model = Post
        exclude = ('views', 'likes', 'comments')

    def create(self, validated_data: dict):
        tags_ids = None
        blog = Blog.objects.filter(id=self.context.get("blog_id", None)).first()

        if 'tags' in validated_data.keys():
            tags_ids = validated_data.pop('tags')

        instance = Post.objects.create(**validated_data)

        if tags_ids:
            instance.tags.set(tags_ids)

        blog.posts.add(instance)

        return instance

    def update(self, instance, validated_data: dict):
        tags_ids = None

        if 'tags' in validated_data.keys():
            tags_ids = validated_data.pop('tags')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_ids is not None:
            instance.tags.set(tags_ids)

        return instance


class PostViewSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class LikePostSerializer(serializers.ModelSerializer):
    CHOICES = (
        ('LK', 'Like'),
        ('ULK', 'Unlike'),
    )
    action = serializers.ChoiceField(choices=CHOICES, read_only=True)

    class Meta:
        model = Post
        fields = ['action', ]

    def update(self, instance, validated_data: dict):
        action = validated_data.get('action', None)
        if action == 'LK':
            instance.likes += 1
        elif action == 'ULK':
            instance.likes -= 1
        instance.save()
        return instance

    def to_internal_value(self, data):
        internal_value = super(LikePostSerializer, self).to_internal_value(data)
        action = data.get("action", None)
        internal_value.update({
            "action": action
        })
        return internal_value


class CommentPostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField()
    body = serializers.CharField()

    class Meta:
        model = Post
        fields = ['author', 'title', 'body']

    def update(self, instance, validated_data: dict):
        comment = Comment.objects.create(**validated_data)
        instance.comments.add(comment)

        return instance
