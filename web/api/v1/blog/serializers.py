from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base64 import b64decode
from django.core.files.base import ContentFile
from django.utils.text import slugify

from transliterate import translit

from blog.models import Article, Category, Comment, Tag, TagArticle
from .services import BlogService
from actions.choices import ActionEvent, ActionMeta
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

    def create(self, validated_data: dict) -> Comment:
        slug = self.context['view'].kwargs['slug']
        article = Article.objects.get(slug=slug)
        validated_data['article'] = article
        comment = super().create(validated_data)
        ActionService(
            event=ActionEvent.CREATE_COMMENT,
            user=validated_data['user'],
            content_object=comment,
            meta=ActionMeta[ActionEvent.CREATE_COMMENT](),
        ).create_action()  # лист активностей
        return comment

    def validate_parent(self, parent: Comment) -> Comment:
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
    is_author = serializers.BooleanField()

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
            'is_author'
        )


class FullArticleSerializer(ArticleSerializer):
    user_like_status = serializers.SerializerMethodField()

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

    def validate_title(self, title):
        translit_title = translit(title, 'ru', reversed=True)
        slug = slugify(translit_title)
        if Article.objects.filter(slug=slug).exists():
            raise serializers.ValidationError({"type_error": "This title already exists."})
        return title

    def create(self, validated_data):
        article = super().create(validated_data)
        ActionService(
            event=ActionEvent.CREATE_ARTICLE,
            user=article.author,
            content_object=article,
            meta=ActionMeta[ActionEvent.CREATE_ARTICLE](),
        ).create_action()  # лист активностей
        service = BlogService()
        service.send_message(article.author)
        service.send_message_for_admin(article.author, article)
        return article


class ArticteUpdateSerializer(serializers.ModelSerializer):
    image = serializers.CharField(allow_blank=True, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'image',
            'category',
            'tags',
        )

    def validate_image(self, image: str):
        if not image:
            return self.instance.image
        mime_type, raw_image = image.split(';base64,')
        image = b64decode(raw_image)
        extention = mime_type.split('/')[-1]
        return ContentFile(image, f'name_image.{extention}')

    @transaction.atomic
    def update(self, instance, validated_data):
        print(f'{self.initial_data=}')

        # tags_id = self.initial_data.getlist('tags', [])
        # TagArticle.objects.filter(article=instance).delete()
        # tags_list = []
        # for tag_id in tags_id:
        #     tag = Tag.objects.get(id=tag_id)
        #     tags_list.append(TagArticle(article=instance, tag=tag))
        # TagArticle.objects.bulk_create(tags_list)
        return super().update(instance, validated_data)
