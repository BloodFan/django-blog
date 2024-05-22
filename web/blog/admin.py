from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Category, Comment, Tag, TagArticle


class TagInline(admin.TabularInline):
    model = TagArticle
    extra = 1
    min_num = 1


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'status', 'author')
    summernote_fields = ('content',)
    fields = (
        'category',
        'title',
        'status',
        'author',
        'image',
        'content',
        'slug',
        'created',
        'updated',
    )
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author')
    list_filter = ('status',)
    inlines = (TagInline,)
    change_form_template = "admin/article/article_changeform.html"

    def response_change(self, request, obj):
        if "_make-active" in request.POST:
            obj.status = True
            obj.save()
            message = 'Blog successfully activated.'
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    list_display = ('id', 'name', 'slug')


@admin.register(TagArticle)
class TagArticleAdmin(admin.ModelAdmin):
    fields = ('tag', 'article')
