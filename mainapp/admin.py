from django.contrib import admin
from .models import Category, Article, Comment, Mark, Repost


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment)
admin.site.register(Mark)
admin.site.register(Repost)
