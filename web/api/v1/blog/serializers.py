from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base64 import b64decode
from django.core.files.base import ContentFile

from blog.models import Article, Category, Comment, Tag
from .services import BlogService
from actions.choices import ActionEvent
from api.v1.actions.services import ActionService
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'image', 'url')


class ChildrenCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'updated')


class CommentSerializer(serializers.ModelSerializer):
    # user_like_status = serializers.SerializerMethodField()
    user_like_status = serializers.IntegerField()
    children = ChildrenCommentSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'updated', 'parent', 'children', 'user_like_status',)

    # def get_user_like_status(self, obj: Comment) -> int:
    #     user = self.context['request'].user
    #     return BlogService.get_user_like_status(user, obj)


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('user', 'content', 'parent')

    def create(self, validated_data):
        slug = self.context['view'].kwargs['slug']
        article = Article.objects.get(slug=slug)
        validated_data['article'] = article
        return super().create(validated_data)

    def validate_parent(self, parent):
        if parent is not None and parent.parent is not None:
            raise ValidationError('Комментарий не может быть parent и children одновременно.')
        if parent is not None and self.context['view'].kwargs['slug'] != parent.article.slug:
            raise ValidationError('Нельзя создать child-comment к комментарию другого article')
        return parent


class TagSerializer(serializers.ModelSerializer):
    """Теги"""
    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'url')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    tags = TagSerializer(many=True, read_only=True)
    up_votes = serializers.IntegerField()
    down_votes = serializers.IntegerField()
    rating = serializers.IntegerField()

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'url',
            'author',
            'category',
            'content',
            'created',
            'updated',
            'comments_count',
            'image',
            'tags',
            'rating',
            'up_votes',
            'down_votes',
        )


class FullArticleSerializer(ArticleSerializer):
    user_like_status = serializers.SerializerMethodField()
    # user_like = serializers.SerializerMethodField(method_name='get_user_like')

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('user_like_status',)

    def to_representation(self, instance):
        representation = super(
            FullArticleSerializer, self
        ).to_representation(instance)
        representation['created'] = instance.created.strftime('%d/%m/%Y')
        return representation

    def get_user_like_status(self, obj: Article) -> int:
        user = self.context['request'].user
        return BlogService.get_user_like_status(user, obj)


class CreateArticleSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Article
        fields = (
            'author',
            'title',
            'category',
            'content',
            'image',
            'tags'
        )

    def validate_image(self, image: str):
        mime_type, raw_image = image.split(';base64,')
        image = b64decode(raw_image)
        extention = mime_type.split('/')[-1]
        return ContentFile(image, f'name_image.{extention}')

    def create(self, validated_data):
        article = super().create(validated_data)
        ActionService(
            event=ActionEvent.CREATE_ARTICLE,
            user=article.author,
            content_object=article
        ).create_action()
        service = BlogService()
        service.send_message(article.author)
        service.send_message_for_admin(article.author, article)
        return article
